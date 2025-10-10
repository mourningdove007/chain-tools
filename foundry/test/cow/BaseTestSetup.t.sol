// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/console.sol";
import {IERC20} from "forge-std/interfaces/IERC20.sol";
import {PublicValues} from "../../src/PublicValues.sol";
import {BaseTest} from "./BaseTest.sol";

contract BaseSetup is BaseTest {
    function testSetup() public view {
        // Initial Wallet Funding for Two Types of Tokens
        assertEq(cow_token.balanceOf(userCow), 10000e18);
        assertEq(dai_token.balanceOf(userDai), 10000e18);

        // Grant Vault Relayer Approval to Spend Tokens
        uint256 currentCowAllowance = cow_token.allowance(
            userCow,
            VAULT_RELAYER_ADDRESS
        );
        uint256 currentDaiAllowance = dai_token.allowance(
            userDai,
            VAULT_RELAYER_ADDRESS
        );
        assertEq(currentCowAllowance, UNLIMITED_ALLOWANCE);
        assertEq(currentDaiAllowance, UNLIMITED_ALLOWANCE);
    }
}
