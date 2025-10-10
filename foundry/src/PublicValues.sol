// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

abstract contract  PublicValues {
    // The DAI token contract address is publically available
    // https://etherscan.io/token/0x6b175474e89094c44da98b954eedeac495271d0f
    address internal constant DAI_TOKEN_ADDRESS = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    
    // The CoW token contract address can be found on etherscan
    // https://etherscan.io/token/0xdef1ca1fb7fbcdc777520aa7f396b4e015f497ab#code
    address internal constant COW_TOKEN_ADDRESS = 0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB;

    // The CoW Settlement Contract
    // https://etherscan.io/address/0x9008D19f58AAbD9eD0D60971565AA8510560ab41
    address internal constant COW_SETTLEMENT_ADDRESS = 0x9008D19f58AAbD9eD0D60971565AA8510560ab41;

    // WETH smart contract can be found on etherscan
    // https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
    address internal constant WETH_TOKEN_ADDRESS = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

    // The Vault Relayer Contract GPv2VaultRelayer.sol
    // https://etherscan.io/address/0xc92e8bdf79f0507f65a392b0ab4667716bfe0110
    address internal constant VAULT_RELAYER_ADDRESS =
        0xC92E8bdf79f0507f65a392b0ab4667716BFE0110;
}
