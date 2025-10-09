// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "forge-std/console.sol";
import {IERC20} from "forge-std/interfaces/IERC20.sol";
import {PublicValues} from "../../src/PublicValues.sol";


interface IWETH is IERC20 {
    function deposit() external payable;
    function withdraw(uint256 wad) external;
}

contract WETHWrapperFuzz is Test, PublicValues {
    IWETH internal weth;
    address internal user;

    function setUp() public {

        vm.createSelectFork("wss://mainnet.gateway.tenderly.co");

        weth = IWETH(PublicValues.WETH_TOKEN_ADDRESS);

        user = makeAddr("AuditorUser");

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
