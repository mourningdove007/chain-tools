import pytest
import subprocess
import time
from web3 import Web3, HTTPProvider

from exceptions.blockchain_exception import BlockchainError

@pytest.fixture(scope="session")
def anvil_instance():

    host = "127.0.0.1"
    port = 8545
    rpc_url = f"http://{host}:{port}"
    mainnet_fork_url = "https://reth-ethereum.ithaca.xyz/rpc"

    ## anvil --chain-id 3 --fork-url https://reth-ethereum.ithaca.xyz/rpc --block-time 1
    anvil_command = ["anvil", "--host", host, "--port", str(port), "--silent", "--chain-id", "3","--fork-url", mainnet_fork_url, "--block-time", "1"]
    
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
                raise BlockchainError(f"Failed to connect to Anvil on {rpc_url} after multiple retries.")
            time.sleep(0.4) # Wait and retry

    yield w3

    print(f"\nStopping Anvil instance (PID: {process.pid})...")
    
    process.terminate()
    
    process.wait(timeout=5) 
    print("Anvil instance stopped successfully.")

