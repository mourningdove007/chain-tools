# Populate Test Accounts

Here we provide instruction to populate a local Anvil chain with wrapped ethereum (WETH), COW Tokens, and USDT.
Hardhat will work but we opt to use Foundry and Anvil because this seems to be the developer's choice for most of these protocols.
After installing foundry, we can start a local instance of the ethereum blockchain:

`anvil --chain-id 3 --fork-url https://reth-ethereum.ithaca.xyz/rpc --block-time 20`

We are forking the current state of the ethereum blockchain.
10 test accounts will be populated each containig 10000 ETH. 
The instance of the blockchain will be listening on `127.0.0.1:8545`
We opt to set the chain id to 3 to be certain we are not targetting the mainnet. 
A block will be mined every 20 seconds.
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
Appropriate environment variables need to be set for `WETH_SMART_CONTRACT` and `PREFUNDED_PUBLIC_KEY`.
The smart contract for WETH is publically available on etherscan. 
Anvil produces 10 prefunded accounts on startup.
```
Available Accounts
==================

(0) 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (10000.000000000000000000 ETH)
(1) 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 (10000.000000000000000000 ETH)
```

We can wrap the tokens of a given test account by running the following command from the root directory:

```
python populate-scripts/wrap_ethereum.py
```

A successful wrapping of tokens results in the following message:

```
http://127.0.0.1:8545
Connecting to RPC URL: http://127.0.0.1:8545
✅ Connection successful!
   Chain ID: 3
   Latest Block: 23487198
Depositing 100 ETH to get WETH...
Successfully deposited ETH. Transaction: 0x0e48dc7c93c5d90976621f9f5799346f4a7facefaaf58a8218824140ecb5f634
Anvil funded account WETH balance: 100 WETH
```

