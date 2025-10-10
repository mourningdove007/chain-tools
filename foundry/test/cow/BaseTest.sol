// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/console.sol";
import {IERC20} from "forge-std/interfaces/IERC20.sol";
import {PublicValues} from "../../src/PublicValues.sol";
import "forge-std/Test.sol";

abstract contract BaseTest is Test, PublicValues {
    uint256 internal constant UNLIMITED_ALLOWANCE = type(uint256).max;

    IERC20 internal cow_token;
    IERC20 internal dai_token;

    address internal userCow;
    address internal userDai;
    address internal solver;

    function setUp() public {
        vm.createSelectFork("wss://mainnet.gateway.tenderly.co");

        cow_token = IERC20(COW_TOKEN_ADDRESS);
        dai_token = IERC20(DAI_TOKEN_ADDRESS);

        userCow = makeAddr("user-1");
        userDai = makeAddr("user-2");
        solver = makeAddr("solver");

        deal(address(DAI_TOKEN_ADDRESS), userDai, 10000e18);
        deal(address(COW_TOKEN_ADDRESS), userCow, 10000e18);

        // Grant Vault Relayer Approval to Spend Tokens
        vm.startPrank(userCow);
        cow_token.approve(VAULT_RELAYER_ADDRESS, UNLIMITED_ALLOWANCE);
        vm.stopPrank();

        vm.startPrank(userDai);
        dai_token.approve(VAULT_RELAYER_ADDRESS, UNLIMITED_ALLOWANCE);
        vm.stopPrank();
    }
}
