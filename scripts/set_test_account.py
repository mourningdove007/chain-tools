import json
import os
from dotenv import load_dotenv

from populate.populate_chain import PopulateChain

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


if __name__ == "__main__":
    print(RPC_URL)

    w3 = PopulateChain.setup_web3_connection(RPC_URL)

    if w3:
        chain_id = w3.eth.chain_id

        print("✅ Connection successful!")
        print(f"   Chain ID: {chain_id}")
        print(f"   Latest Block: {w3.eth.block_number}")

        PopulateChain.get_weth(100, w3, WETH_SMART_CONTRACT, ACCOUNT_PUBLIC_KEY)
