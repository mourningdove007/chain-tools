// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "forge-std/console.sol";
import {IERC20} from "forge-std/interfaces/IERC20.sol";

contract FundAccount is Test {

    // The DAI token contract address is publically available
    // https://etherscan.io/token/0x6b175474e89094c44da98b954eedeac495271d0f
    address internal constant DAI_TOKEN_ADDRESS = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    
    uint256 internal constant TRANSFER_AMOUNT = 10000e18; 
    
    IERC20 internal dai_token;

    address internal receiveWallet;
    address internal senderWallet;


    function setUp() public {

        dai_token = IERC20(DAI_TOKEN_ADDRESS);
        vm.label(DAI_TOKEN_ADDRESS, "DAI Token");

        receiveWallet = makeAddr("recevie-wallet");
        senderWallet = makeAddr("sender-wallet");

        vm.createSelectFork("wss://mainnet.gateway.tenderly.co");

        deal(address(DAI_TOKEN_ADDRESS), senderWallet, 10000e18);

    }


    function testSuccessfulDeal() public {
        assertEq(dai_token.balanceOf(senderWallet), 10000e18);   
    }


    function testSuccessfulTokenTransfer() public {
        
        uint256 senderInitialBalance = dai_token.balanceOf(senderWallet);
        uint256 recipientInitialBalance = dai_token.balanceOf(receiveWallet);
        
        console2.log("Initial Sender Balance:", senderInitialBalance);
        console2.log("Initial Recipient Balance:", recipientInitialBalance);
        
        vm.startPrank(senderWallet);
        bool success = dai_token.transfer(receiveWallet, TRANSFER_AMOUNT);
        vm.stopPrank();

        assertTrue(success, "Token transfer call must return true");

        uint256 senderFinalBalance = dai_token.balanceOf(senderWallet);
        uint256 recipientFinalBalance = dai_token.balanceOf(receiveWallet);
        
        console2.log("Final Sender Balance:", senderFinalBalance);
        console2.log("Final Recipient Balance:", recipientFinalBalance);

        assertEq(
            senderFinalBalance, 
            senderInitialBalance - TRANSFER_AMOUNT, 
            "Sender's final balance is incorrect"
        );
        
        assertEq(
            recipientFinalBalance, 
            recipientInitialBalance + TRANSFER_AMOUNT, 
            "Recipient's final balance is incorrect"
        );
    }

}