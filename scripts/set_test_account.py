from constants.blockchain import BlockchainAddresses as ba
from populate.populate_chain import PopulateChain as pc

if __name__ == "__main__":

    pc.fund_account_with_dai_and_weth(
        ba.ANVIL_RPC_URL, 
        ba.WETH_CONTRACT, 
        ba.DAI_WHALE, 
        ba.ANVIL_TEST_ACCOUNT_1
        )
