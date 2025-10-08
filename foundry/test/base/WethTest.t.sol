// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "forge-std/console.sol";
import {MockERC20} from "../../src/MockToken.sol";

contract WETHWrapperFuzz is Test {
    MockERC20 internal weth;
    address internal user;

    function setUp() public {
        weth = new MockERC20("Wrapped Ether", "WETH");

        user = makeAddr("AuditorUser");

        vm.deal(user, type(uint256).max);
    }

    function testFuzz_WETHBalanceIsCorrectAfterDeposit(
        uint256 ethToDeposit
    ) public {
        if (ethToDeposit == 0) {
            return;
        }

        uint256 initialEth = user.balance;
        uint256 initialWEth = weth.balanceOf(user);

        vm.startPrank(user);

        try weth.deposit{value: ethToDeposit}() {} catch {}

        vm.stopPrank();

        uint256 finalWeth = weth.balanceOf(user);

        uint256 spentEth = initialEth - user.balance;

        assertEq(
            finalWeth - initialWEth,
            spentEth,
            "WETH received must match ETH spent."
        );
    }
}
