import json
from web3 import Web3
from web3.contract import Contract

from exceptions.blockchain_exception import BlockchainError

ERC20_ABI = json.loads(
    """[
    {"constant": true,"inputs": [],"name": "name","outputs": [{"name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},
    {"constant": false,"inputs": [{"name": "_to","type": "address"},{"name": "_value","type": "uint256"}],"name": "transfer","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},
    {"constant": true,"inputs": [{"name": "_owner","type": "address"}],"name": "balanceOf","outputs": [{"name": "balance","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},
    {"constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}
]"""
)


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
    def get_weth(
        amount: int, w3: Web3, weth_smart_contract: str, account_public_key: str
    ) -> Contract:
        print(f"Depositing {amount} ETH to get WETH...")
        weth_contract: Contract = w3.eth.contract(
            address=w3.to_checksum_address(weth_smart_contract), abi=ERC20_ABI
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
