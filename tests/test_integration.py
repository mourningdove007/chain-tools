import random
import pytest
from web3 import Web3, HTTPProvider
import time
from constants.blockchain import BlockchainAddresses as ba
from exceptions.blockchain_exception import BlockchainError
from populate.populate_chain import PopulateChain
from web3.contract import Contract
import subprocess


class TestIntegration:

    @pytest.fixture(scope="class", autouse=True)
    def anvil_instance(self):

        host = "127.0.0.1"
        port = 8545
        rpc_url = f"http://{host}:{port}"
        mainnet_fork_url = "https://reth-ethereum.ithaca.xyz/rpc"

        ## anvil --chain-id 3 --fork-url https://reth-ethereum.ithaca.xyz/rpc --block-time 1
        anvil_command = [
            "anvil",
            "--host",
            host,
            "--port",
            str(port),
            "--silent",
            "--chain-id",
            "3",
            "--fork-url",
            mainnet_fork_url,
            "--block-time",
            "1",
        ]

        print(f"\nStarting Anvil instance on {rpc_url}...")

        try:
            process = subprocess.Popen(
                anvil_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError:
            raise Exception(
                "Anvil command not found. Ensure the 'anvil' CLI tool is installed (e.g., via 'cargo install anvil') and accessible in your system's PATH."
            )

        w3 = Web3(HTTPProvider(rpc_url))
        max_retries = 15
        for i in range(max_retries):
            try:
                if w3.is_connected():
                    print("Anvil is running and connected.")
                    break
            except Exception:
                if i == max_retries - 1:
                    process.terminate()
                    raise BlockchainError(
                        f"Failed to connect to Anvil on {rpc_url} after multiple retries."
                    )
                time.sleep(0.4)  # Wait and retry

        yield w3

        print(f"\nStopping Anvil instance (PID: {process.pid})...")

        process.terminate()

        process.wait(timeout=5)
        print("Anvil instance stopped successfully.")

    def test_failed_set_up_connection(self):
        with pytest.raises(BlockchainError):
            PopulateChain.setup_web3_connection(ba.ANVIL_RPC_URL)

    def test_successful_wrapped_ETH(self, anvil_instance):

        time.sleep(3)  ## requires fixture to start

        amount = random.randint(2, 4000)

        w3: Web3 = PopulateChain.setup_web3_connection(ba.ANVIL_RPC_URL)
        pc = PopulateChain(ba.ANVIL_RPC_URL)
        weth_contract = pc.wrap_ether(amount, ba.ANVIL_TEST_ACCOUNT_1)

        eth_balance = weth_contract.functions.balanceOf(
            w3.to_checksum_address(ba.ANVIL_TEST_ACCOUNT_1)
        ).call()

        weth_balance = w3.from_wei(eth_balance, "ether")

        assert weth_balance == amount

    def test_fund_dai(self, anvil_instance):

        time.sleep(3)  ## requires fixture to start

        amount = random.randint(2, 4000)

        w3: Web3 = PopulateChain.setup_web3_connection(ba.ANVIL_RPC_URL)
        pc = PopulateChain(ba.ANVIL_RPC_URL)

        dai_contract: Contract = w3.eth.contract(
            address=w3.to_checksum_address(ba.DAI_CONTRACT), abi=ba.ERC20_ABI
        )

        initial_eth_balance = dai_contract.functions.balanceOf(
            w3.to_checksum_address(ba.ANVIL_TEST_ACCOUNT_1)
        ).call()

        pc.fund_whale_for_testing(101)
        pc.fund_dai_account(amount, ba.ANVIL_TEST_ACCOUNT_1)

        final_eth_balance = dai_contract.functions.balanceOf(
            w3.to_checksum_address(ba.ANVIL_TEST_ACCOUNT_1)
        ).call()

        actual_balance = int(w3.from_wei(final_eth_balance, "ether"))
        expected_balance = int(initial_eth_balance + amount)

        assert actual_balance == expected_balance
