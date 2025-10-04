import random
import pytest
from web3 import Web3
import time
from constants.blockchain import BlockchainAddresses as ba
from exceptions.blockchain_exception import BlockchainError
from populate.populate_chain import PopulateChain as pc


class TestWrappedEthereum:

    def test_failed_set_up_connection(self):
        with pytest.raises(BlockchainError):
            pc.setup_web3_connection(ba.ANVIL_RPC_URL)

    def test_successful_wrapped_ETH(self, anvil_instance):

        time.sleep(2)  ## requires fixture to start

        amount = random.randint(2, 4000)

        w3: Web3 = pc.setup_web3_connection(ba.ANVIL_RPC_URL)
        weth_contract = pc.wrap_ether(
            amount, w3, ba.WETH_CONTRACT, ba.ANVIL_TEST_ACCOUNT_1
        )

        eth_balance = weth_contract.functions.balanceOf(
            w3.to_checksum_address(ba.ANVIL_TEST_ACCOUNT_1)
        ).call()

        weth_balance = w3.from_wei(eth_balance, "ether")

        assert weth_balance == amount
