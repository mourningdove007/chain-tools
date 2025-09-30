## Populate Test Accounts

Here we provide instruction to populate a local Anvil chain with wrapped ethereum (WETH) and USDT.
Hardhat will work but we opt to use Foundry and Anvil because this seems to be the developer's choice for most of these protocols.
After installing foundry, we can start a local instance of the ethereum blockchain:

`anvil --fork-url https://reth-ethereum.ithaca.xyz/rpc`

Notice we are forking the current state of the ethereum blockchain.
10 test accounts will be populated each containig 10000 ETH. 
The instance of the blockchain will be listening on `127.0.0.1:8545`

