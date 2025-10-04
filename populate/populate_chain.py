import time
from typing import Union
from web3 import Web3
from web3.contract import Contract

from constants.blockchain import BlockchainAddresses as ba
from exceptions.blockchain_exception import BlockchainError


class PopulateChain:

    @staticmethod
    def setup_web3_connection(rpc_url: str) -> Web3:
        print(f"Connecting to RPC URL: {rpc_url}")
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        if not w3.is_connected():
            print("Error: Failed to connect to Web3 provider.")
            raise BlockchainError("Failed to connect to Web3 provider.")

        return w3

    @staticmethod
    def wrap_ether(
        amount: int, w3: Web3, weth_smart_contract: str, account_public_key: str
    ) -> Contract:
        print(f"Depositing {amount} ETH to get WETH...")
        weth_contract: Contract = w3.eth.contract(
            address=w3.to_checksum_address(weth_smart_contract), abi=ba.ERC20_ABI
        )
        tx_hash = weth_contract.functions.deposit().transact(
            {
                "from": w3.to_checksum_address(account_public_key),
                "value": w3.to_wei(amount, "ether"),
            }
        )

        w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Successfully deposited ETH. Transaction: {w3.to_hex(tx_hash)}")
        return weth_contract

    def fund_dai_account(
        amount: Union[int, float],
        w3: Web3,
        whale_address: str,
        test_account_address: str,
    ):

        amount_wei = w3.to_wei(amount, "ether")

        print(f"\n🐋 Impersonating DAI Whale: {whale_address}")
        try:
            w3.provider.make_request(
                method="hardhat_impersonateAccount",
                params=[w3.to_checksum_address(whale_address)],
            )
            dai_contract: Contract = w3.eth.contract(
                address=w3.to_checksum_address(ba.DAI_CONTRACT), abi=ba.ERC20_ABI
            )
        except Exception as e:
            print(
                f"🚨 WARNING: Could not impersonate account. Ensure Anvil is running with correct flags. Error: {e}"
            )
            return

        print(f"💰 Transferring {amount} DAI (Wei amount: {amount_wei})...")

        initial_dai_wei = dai_contract.functions.balanceOf(
            w3.to_checksum_address(test_account_address)
        ).call()
        print(f"Initial Balance: {initial_dai_wei:.4f} WEI (DAI)")

        target_wei = initial_dai_wei + amount_wei

        tx_hash = dai_contract.functions.transfer(
            w3.to_checksum_address(test_account_address), amount_wei
        ).transact(
            {
                "from": w3.to_checksum_address(whale_address),
            }
        )

        w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Transfer successful! Tx Hash: {w3.to_hex(tx_hash)}")

        final_balance_wei = dai_contract.functions.balanceOf(
            w3.to_checksum_address(test_account_address)
        ).call()
        final_balance_dai = w3.from_wei(final_balance_wei, "ether")

        if int(final_balance_wei) == int(target_wei):
            print(f"🎉 Final DAI Balance: {final_balance_dai:.2f} DAI.")
            print("Test account successfully funded.")
        else:
            raise Exception(
                f"Transfer failed verification. Expected {w3.from_wei(target_wei, 'ether')}, got {final_balance_dai}"
            )

    @staticmethod
    def fund_whale_for_testing(amount_eth: float, w3: Web3, whale_address: str):

        dest_checksum = w3.to_checksum_address(whale_address)
        amount_wei = w3.to_wei(amount_eth, "ether")

        print("-" * 50)
        print(
            f"Attempting to fund whale {whale_address[:8]}... with {amount_eth:.4f} ETH."
        )

        initial_wei = w3.eth.get_balance(dest_checksum)
        initial_eth = w3.from_wei(initial_wei, "ether")
        print(f"Initial Balance: {initial_eth:.4f} ETH")

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
                print(f"✅ Funding successful. Anvil RPC call completed.")
                print(f"Whale's New ETH Balance: {final_eth:.4f} ETH.")
            else:
                print(f"⚠️ Balance change failed or RPC method was not available.")

        except Exception as e:
            print(f"❌ Funding failed. Is your Anvil instance running?")
            print(f"RPC Error: {e}")

        print("-" * 50)

    def fund_account_with_dai_and_weth(
        rpc_url: str,
        weth_smart_contract: str,
        whale_address: str,
        test_account_address: str,
    ):

        w3 = PopulateChain.setup_web3_connection(rpc_url)

        if w3:
            chain_id = w3.eth.chain_id

            print("✅ Connection successful!")
            print(f"   Chain ID: {chain_id}")
            print(f"   Latest Block: {w3.eth.block_number}")

            PopulateChain.wrap_ether(100, w3, weth_smart_contract, test_account_address)
            PopulateChain.fund_whale_for_testing(10, w3, whale_address)
            PopulateChain.fund_dai_account(
                10000, w3, whale_address, test_account_address
            )
