import json
import os
from dotenv import load_dotenv
from web3 import Web3
from web3.contract import Contract

load_dotenv(".env")

RPC_URL = os.getenv("RPC_URL")
ACCOUNT_PRIVATE_KEY = os.getenv("PRIVATE_KEY_WETH")
ACCOUNT_PUBLIC_KEY = os.getenv("PUBLIC_KEY_WETH")

ERC20_ABI = json.loads('''[
    {"constant": true,"inputs": [],"name": "name","outputs": [{"name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},
    {"constant": false,"inputs": [{"name": "_to","type": "address"},{"name": "_value","type": "uint256"}],"name": "transfer","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},
    {"constant": true,"inputs": [{"name": "_owner","type": "address"}],"name": "balanceOf","outputs": [{"name": "balance","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},
    {"constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}
]''')

def setup_web3_connection():
    print(f"Connecting to RPC URL: {RPC_URL}")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    if not w3.is_connected():
        print("Error: Failed to connect to Web3 provider.")
        return None
        
    return w3

def get_weth(w3: Web3):
    """Deposits ETH to get WETH and sends it to the specified address."""
    print(f"Depositing {5} ETH to get WETH...")
    
    weth_contract: Contract = w3.eth.contract(address=w3.to_checksum_address(ACCOUNT_PUBLIC_KEY), abi=ERC20_ABI)
    
    print(f"Contract: {str(weth_contract)}")
    

if __name__ == "__main__":  
    print(RPC_URL)

    w3 = setup_web3_connection()
    
    if w3:
        chain_id = w3.eth.chain_id
        
        print("✅ Connection successful!")
        print(f"   Chain ID: {chain_id}")
        print(f"   Seller Wallet Address (from .env): {str(ACCOUNT_PRIVATE_KEY)}")
        print(f"   Latest Block: {w3.eth.block_number}")

        print(get_weth(w3))
