import random
import pytest
from web3 import Web3
import time
from exceptions.blockchain_exception import BlockchainError
from populate.populate_chain import PopulateChain as pc


class TestWrappedEthereum:

    host = "127.0.0.1"
    port = 8545
    rpc_url = f"http://{host}:{port}"

    ## WETH Smart Contract can be found on etherscan
    ## https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
    ## Anvil creates prefunded accounts
    ## Do not use the prefunded accounts in a production environment
    ## These are very well known keys and anything sent to them will likely be stolen

    weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    test_account_public_key = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

    def test_failed_set_up_connection(self):
        with pytest.raises(BlockchainError):
            pc.setup_web3_connection(self.rpc_url)

    def test_successful_wrapped_ETH(self, anvil_instance):

        time.sleep(2)  ## requires fixture to start

        amount = random.randint(2, 4000)

        w3: Web3 = pc.setup_web3_connection(self.rpc_url)
        weth_contract = pc.get_weth(
            amount, w3, self.weth_address, self.test_account_public_key
        )

        eth_balance = weth_contract.functions.balanceOf(
            w3.to_checksum_address(self.test_account_public_key)
        ).call()

        weth_balance = w3.from_wei(eth_balance, "ether")

        assert weth_balance == amount
