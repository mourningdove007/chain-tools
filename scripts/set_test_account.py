from constants.blockchain import BlockchainAddresses as ba
from populate.populate_chain import PopulateChain

if __name__ == "__main__":

    pc = PopulateChain(ba.ANVIL_RPC_URL)
    pc.fund_account_with_dai_and_weth(ba.ANVIL_TEST_ACCOUNT_1)
