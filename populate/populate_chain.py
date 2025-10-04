import time
from typing import Union
from web3 import Web3
from web3.contract import Contract

from constants.blockchain import BlockchainAddresses as ba
from exceptions.blockchain_exception import BlockchainError
from utility.logging import (
    print_green,
    print_info,
    print_red,
    print_whale,
    print_yellow,
)


class PopulateChain:

    def __init__(self, rpc_url: str):
        self.w3: Web3 = PopulateChain.setup_web3_connection(rpc_url)
        print_info(f"Web3 connection established successfully to {rpc_url}.")

    @staticmethod
    def setup_web3_connection(rpc_url: str) -> Web3:
        print_info(f"Connecting to RPC URL: {rpc_url}")
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        if not w3.is_connected():
            print_red("Error: Failed to connect to Web3 provider.")
            raise BlockchainError("Failed to connect to Web3 provider.")

        return w3

    def wrap_ether(self, amount: int, account_public_key: str) -> Contract:
        print_info(f"Depositing {amount} ETH to get WETH...")
        w3 = self.w3
        weth_contract: Contract = w3.eth.contract(
            address=w3.to_checksum_address(ba.WETH_CONTRACT), abi=ba.ERC20_ABI
        )
        tx_hash = weth_contract.functions.deposit().transact(
            {
                "from": w3.to_checksum_address(account_public_key),
                "value": w3.to_wei(amount, "ether"),
            }
        )

        w3.eth.wait_for_transaction_receipt(tx_hash)
        print_green(f"Successfully deposited ETH. Transaction: {w3.to_hex(tx_hash)}")
        return weth_contract

    def fund_dai_account(
        self,
        amount: Union[int, float],
        test_account_address: str,
    ):

        w3 = self.w3
        amount_wei = w3.to_wei(amount, "ether")

        print_whale(f"\nImpersonating DAI 🐋: {ba.DAI_WHALE}")
        try:
            w3.provider.make_request(
                method="hardhat_impersonateAccount",
                params=[w3.to_checksum_address(ba.DAI_WHALE)],
            )
            dai_contract: Contract = w3.eth.contract(
                address=w3.to_checksum_address(ba.DAI_CONTRACT), abi=ba.ERC20_ABI
            )
        except Exception as e:
            print_yellow(
                f"WARNING: Could not impersonate account. Ensure Anvil is running with correct flags. Error: {e}"
            )
            return

        print_info(f"Transferring {amount} DAI ...")

        initial_dai_wei = dai_contract.functions.balanceOf(
            w3.to_checksum_address(test_account_address)
        ).call()
        print_info(f"Initial Balance: {initial_dai_wei:.4f} WEI (DAI)")

        target_wei = initial_dai_wei + amount_wei

        tx_hash = dai_contract.functions.transfer(
            w3.to_checksum_address(test_account_address), amount_wei
        ).transact(
            {
                "from": w3.to_checksum_address(ba.DAI_WHALE),
            }
        )

        w3.eth.wait_for_transaction_receipt(tx_hash)
        print_green(f"Transfer successful! Tx Hash: {w3.to_hex(tx_hash)}")

        final_balance_wei = dai_contract.functions.balanceOf(
            w3.to_checksum_address(test_account_address)
        ).call()
        final_balance_dai = w3.from_wei(final_balance_wei, "ether")

        if int(final_balance_wei) == int(target_wei):
            print_info(f"Final DAI Balance: {final_balance_dai:.2f} DAI.")
            print_green("Test account successfully funded.")
        else:
            raise Exception(
                f"Transfer failed verification. Expected {w3.from_wei(target_wei, 'ether')}, got {final_balance_dai}"
            )

    def fund_whale_for_testing(self, amount_eth: float):

        w3 = self.w3
        dest_checksum = w3.to_checksum_address(ba.DAI_WHALE)
        amount_wei = w3.to_wei(amount_eth, "ether")

        print_info("-" * 50)
        print_info(
            f"Attempting to fund whale {ba.DAI_WHALE[:8]}... with {amount_eth:.4f} ETH."
        )

        initial_wei = w3.eth.get_balance(dest_checksum)
        initial_eth = w3.from_wei(initial_wei, "ether")
        print_info(f"Initial Balance: {initial_eth:.4f} ETH")

        target_wei = initial_wei + amount_wei

        target_wei_hex = hex(target_wei)

        try:

            w3.provider.make_request(
                "anvil_setBalance", [dest_checksum, target_wei_hex]
            )

            time.sleep(0.5)

            final_wei = w3.eth.get_balance(dest_checksum)
            final_eth = w3.from_wei(final_wei, "ether")

            if final_eth == (initial_eth + amount_eth):
                print_green(f"Funding successful. Anvil RPC call completed.")
                print_info(f"Whale's New ETH Balance: {final_eth:.4f} ETH.")
            else:
                print_yellow(f"Balance change failed or RPC method was not available.")

        except Exception as e:
            print_red(f"Funding failed. Is your Anvil instance running?")
            print_red(f"RPC Error: {e}")

        print_info("-" * 50)

    def fund_account_with_dai_and_weth(
        self,
        test_account_address: str,
    ):

        w3 = self.w3

        if w3:
            chain_id = w3.eth.chain_id

            print_green("Connection successful!")
            print_info(f"   Chain ID: {chain_id}")
            print_info(f"   Latest Block: {w3.eth.block_number}")

            self.wrap_ether(100, test_account_address)
            self.fund_whale_for_testing(101)
            self.fund_dai_account(102, test_account_address)
