// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import {IERC20} from "forge-std/interfaces/IERC20.sol";
import {PublicValues} from "../../src/PublicValues.sol";

contract ApprovalTest is Test, PublicValues {
    using Strings for uint256;
    uint256 internal constant UNLIMITED_ALLOWANCE = type(uint256).max;
    address internal userWallet;

    IERC20 internal weth;
    IERC20 internal dai;

    function setUp() public {
        vm.createSelectFork("wss://mainnet.gateway.tenderly.co");

        userWallet = makeAddr("user-wallet");

        weth = IERC20(PublicValues.WETH_TOKEN_ADDRESS);

        dai = IERC20(PublicValues.DAI_TOKEN_ADDRESS);

        console.log("User Wallet:", userWallet);
        console.log("Vault Relayer:", VAULT_RELAYER_ADDRESS);
        console.log("WETH Contract:", address(weth));
    }

    function testGrantUnlimitedApproval() public {
        vm.startPrank(userWallet);

        weth.approve(VAULT_RELAYER_ADDRESS, UNLIMITED_ALLOWANCE);

        vm.stopPrank();

        uint256 currentAllowance = weth.allowance(
            userWallet,
            VAULT_RELAYER_ADDRESS
        );

        assertEq(
            currentAllowance,
            UNLIMITED_ALLOWANCE,
            "Unlimited allowance should be granted to the Vault Relayer"
        );
        console.log("Unlimited WETH allowance verified: PASSED");
    }

    function testGrantLimitedApproval() public {
        uint256 limitedAmount = 1_000 * 10 ** 6;

        vm.startPrank(userWallet);

        dai.approve(VAULT_RELAYER_ADDRESS, limitedAmount);

        vm.stopPrank();

        uint256 currentAllowance = dai.allowance(
            userWallet,
            VAULT_RELAYER_ADDRESS
        );

        string memory currentString = currentAllowance.toString();
        string memory limitedString = limitedAmount.toString();

        string memory successMessage = string(
            abi.encodePacked(
                "\n",
                "\n",
                "Current Allowance: ",
                currentString,
                "\n",
                "Limited Amount: ",
                limitedString,
                "\n",
                "Limited DAI allowance verified: PASSED"
            )
        );

        assertEq(currentAllowance, limitedAmount, successMessage);
        console.log(successMessage);
    }
}
