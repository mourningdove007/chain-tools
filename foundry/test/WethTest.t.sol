// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "forge-std/console.sol";

interface IWETH {
    function deposit() external payable;
    function balanceOf(address account) external view returns (uint256);
}

contract MockWETH is IWETH {
    mapping(address => uint256) public balances;

    function deposit() external payable override {
        balances[msg.sender] += msg.value;
    }

    function balanceOf(
        address account
    ) external view override returns (uint256) {
        return balances[account];
    }
}

contract WETHWrapperFuzz is Test {
    IWETH internal weth;
    address internal user;

    function setUp() public {
        weth = new MockWETH();

        user = makeAddr("AuditorUser");

        vm.deal(user, type(uint256).max);
    }

    function testFuzz_WETHBalanceIsCorrectAfterDeposit(
        uint256 ethToDeposit
    ) public {
        if (ethToDeposit == 0) {
            return;
        }

        uint256 initialETH = user.balance;
        uint256 initialWETH = weth.balanceOf(user);

        vm.startPrank(user);

        try weth.deposit{value: ethToDeposit}() {} catch {}

        vm.stopPrank();

        uint256 finalWETH = weth.balanceOf(user);

        uint256 spentETH = initialETH - user.balance;

        assertEq(
            finalWETH - initialWETH,
            spentETH,
            "WETH received must match ETH spent."
        );
    }
}
