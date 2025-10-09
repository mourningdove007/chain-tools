// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import {IERC20} from "forge-std/interfaces/IERC20.sol";


contract ApprovalTest is Test {

    using Strings for uint256;
    
    address internal constant VAULT_RELAYER_ADDRESS =
        0xC92E8bdf79f0507f65a392b0ab4667716BFE0110;
    uint256 internal constant UNLIMITED_ALLOWANCE = type(uint256).max;
    address internal userWallet;

    
    IERC20 internal weth;
    IERC20 internal dai;

    function setUp() public {
        vm.createSelectFork("wss://mainnet.gateway.tenderly.co");

        userWallet = makeAddr("user-wallet");

        // WETH smart contract can be found on etherscan
        // https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
        weth = IERC20(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);

        // The DAI token contract address is publically available
        // https://etherscan.io/token/0x6b175474e89094c44da98b954eedeac495271d0f
        dai = IERC20(0x6B175474E89094C44Da98b954EedeAC495271d0F);

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

        string memory successMessage = string(abi.encodePacked(
            "\n",
            "\n",
            "Current Allowance: ",
            currentString,
            "\n",
            "Limited Amount: ",
            limitedString,
            "\n",
            "Limited DAI allowance verified: PASSED" 
        ));
    

        assertEq(
            currentAllowance,
            limitedAmount,
            successMessage
        );
        console.log(successMessage);
    }
}
