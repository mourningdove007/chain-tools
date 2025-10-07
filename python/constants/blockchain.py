import json


class BlockchainAddresses:

    ## DAI smart contract can be found on etherscan
    ## https://etherscan.io/token/0x6b175474e89094c44da98b954eedeac495271d0f
    DAI_CONTRACT: str = "0x6b175474e89094c44da98b954eedeac495271d0f"

    ## WETH smart contract can be found on etherscan
    ## https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
    WETH_CONTRACT: str = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

    ## DAI whale holder can be viewed on etherscan
    ## https://etherscan.io/token/0x6b175474e89094c44da98b954eedeac495271d0f#balances
    DAI_WHALE: str = "0x40ec5B33f54e0E8A33A975908C5BA1c14e5BbbDf"

    ## Do not use the prefunded accounts in a production environment
    ## These are very well known keys and anything sent to them will likely be stolen
    ANVIL_TEST_ACCOUNT_1: str = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    ANVIL_TEST_ACCOUNT_2: str = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    ANVIL_TEST_ACCOUNT_1_SECRET: str = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    ANVIL_TEST_ACCOUNT_2_SECRET: str = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

    ANVIL_RPC_URL: str = "http://127.0.0.1:8545"
    ORDERS_URL: str = "http://localhost:8080/api/v1/orders"

    HEADERS = {'accept': 'application/json'}

    ERC20_ABI = json.loads(
        """[
        {"constant": true,"inputs": [],"name": "name","outputs": [{"name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},
        {"constant": false,"inputs": [{"name": "_to","type": "address"},{"name": "_value","type": "uint256"}],"name": "transfer","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},
        {"constant": true,"inputs": [{"name": "_owner","type": "address"}],"name": "balanceOf","outputs": [{"name": "balance","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},
        {"constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}
    ]"""
    )
