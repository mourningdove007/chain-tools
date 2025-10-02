import json
import os
from dotenv import load_dotenv
from web3 import Web3
from web3.contract import Contract

load_dotenv(".env")

RPC_URL = os.getenv("RPC_URL")
ACCOUNT_PUBLIC_KEY = os.getenv("PREFUNDED_PUBLIC_KEY")
WETH_SMART_CONTRACT = os.getenv("WETH_SMART_CONTRACT")

ERC20_ABI = json.loads(
    """[
    {"constant": true,"inputs": [],"name": "name","outputs": [{"name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},
    {"constant": false,"inputs": [{"name": "_to","type": "address"},{"name": "_value","type": "uint256"}],"name": "transfer","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},
    {"constant": true,"inputs": [{"name": "_owner","type": "address"}],"name": "balanceOf","outputs": [{"name": "balance","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},
    {"constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}
]"""
)


def setup_web3_connection():
    print(f"Connecting to RPC URL: {RPC_URL}")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not w3.is_connected():
        print("Error: Failed to connect to Web3 provider.")
        return None

    return w3


def get_weth(w3: Web3):
    print(f"Depositing {100} ETH to get WETH...")
    weth_contract: Contract = w3.eth.contract(
        address=w3.to_checksum_address(WETH_SMART_CONTRACT), abi=ERC20_ABI
    )
    tx_hash = weth_contract.functions.deposit().transact(
        {
            "from": w3.to_checksum_address(ACCOUNT_PUBLIC_KEY),
            "value": w3.to_wei(100, "ether"),
        }
    )

    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Successfully deposited ETH. Transaction: {w3.to_hex(tx_hash)}")

    weth_balance = weth_contract.functions.balanceOf(
        w3.to_checksum_address(ACCOUNT_PUBLIC_KEY)
    ).call()
    print(
        f"Anvil funded account WETH balance: {w3.from_wei(weth_balance, 'ether')} WETH"
    )


if __name__ == "__main__":
    print(RPC_URL)

    w3 = setup_web3_connection()

    if w3:
        chain_id = w3.eth.chain_id

        print("✅ Connection successful!")
        print(f"   Chain ID: {chain_id}")
        print(f"   Latest Block: {w3.eth.block_number}")

        get_weth(w3)
