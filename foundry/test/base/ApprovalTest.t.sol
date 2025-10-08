// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import {MockERC20} from "../../src/MockToken.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract ApprovalTest is Test {

    using Strings for uint256;
    
    address internal constant VAULT_RELAYER_ADDRESS =
        0xC92E8bdf79f0507f65a392b0ab4667716BFE0110;
    uint256 internal constant UNLIMITED_ALLOWANCE = type(uint256).max;
    address internal userWallet;

    
    MockERC20 internal weth;
    MockERC20 internal usdc;

    function setUp() public {
        userWallet = makeAddr("user-wallet");

        weth = new MockERC20("Wrapped Ether", "WETH");
        usdc = new MockERC20("USD Coin", "USDC");

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

        usdc.approve(VAULT_RELAYER_ADDRESS, limitedAmount);

        vm.stopPrank();

        uint256 currentAllowance = usdc.allowance(
            userWallet,
            VAULT_RELAYER_ADDRESS
        );

        string memory currentString = currentAllowance.toString();
        string memory limitedString = limitedAmount.toString();

        string memory successMessage = string(abi.encodePacked(
            "\n",
            "\n",
            "Current Allowance: ",
            currentString,
            "\n",
            "Limited Amount: ",
            limitedString,
            "\n",
            "Limited USDC allowance verified: PASSED" 
        ));
    

        assertEq(
            currentAllowance,
            limitedAmount,
            successMessage
        );
        console.log(successMessage);
    }
}
