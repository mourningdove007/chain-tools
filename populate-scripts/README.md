# Populate Test Accounts

Here we provide instruction to populate a local Anvil chain with wrapped ethereum (WETH), COW Tokens, and USDT.
Hardhat will work but we opt to use Foundry and Anvil because this seems to be the developer's choice for most of these protocols.
After installing foundry, we can start a local instance of the ethereum blockchain:

`anvil --chain-id 3 --fork-url https://reth-ethereum.ithaca.xyz/rpc`

We are forking the current state of the ethereum blockchain.
10 test accounts will be populated each containig 10000 ETH. 
The instance of the blockchain will be listening on `127.0.0.1:8545`
We opt to set the chain id to 3 to be certain we are not targetting the mainnet. 
This ID can be checked using `cast`.

```
cast chain-id
```

Notice the terminal attached to the anvil blockchain will log that the chain ID was checked.

```
Listening on 127.0.0.1:8545
eth_chainId
```


## Wrapped Ethereum (WETH)

To use our ETH in a decentralized protocol, we must wrap the token in WETH which is an ERC-20-complient token.
We can wrap the tokens of a given test account by running the following command from the root directory:

```
python populate-scripts/wrap_ethereum.py
```

