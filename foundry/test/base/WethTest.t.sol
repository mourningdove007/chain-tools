// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "forge-std/console.sol";
import {IERC20} from "forge-std/interfaces/IERC20.sol";


interface IWETH is IERC20 {
    function deposit() external payable;
    function withdraw(uint256 wad) external;
}

contract WETHWrapperFuzz is Test {
    IWETH internal weth;
    address internal user;

    function setUp() public {

        vm.createSelectFork("wss://mainnet.gateway.tenderly.co");

        // WETH smart contract can be found on etherscan
        // https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
        weth = IWETH(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);

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
