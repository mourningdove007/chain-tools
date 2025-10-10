// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import {Script, console2} from "forge-std/Script.sol";
import {IERC20} from "forge-std/interfaces/IERC20.sol";
import {PublicValues} from "../src/PublicValues.sol";


interface IWETH is IERC20 {
    function deposit() external payable;
    function withdraw(uint256 wad) external;
}


contract SimpleScript is Script, PublicValues{

    
    uint256 internal constant UNLIMITED_ALLOWANCE = type(uint256).max;
    IWETH internal weth;
    IERC20 internal cow_token;
    IERC20 internal dai_token;

    address internal userCow;
    address internal userDai;
    address internal solver;

    function run() public {

        cow_token = IERC20(COW_TOKEN_ADDRESS);
        dai_token = IERC20(DAI_TOKEN_ADDRESS);
        weth = IWETH(PublicValues.WETH_TOKEN_ADDRESS);


        userCow = makeAddr("userCow");
        userDai = ANVIL_TEST_ACCOUNT_2;
        solver = makeAddr("solver");

        vm.deal(address(PublicValues.DAI_TOKEN_ADDRESS), 100 ether);

        vm.startPrank(userDai);
        cow_token.approve(VAULT_RELAYER_ADDRESS, UNLIMITED_ALLOWANCE);
        dai_token.approve(VAULT_RELAYER_ADDRESS, UNLIMITED_ALLOWANCE);
        weth.deposit{value: 100 ether}();
        vm.stopPrank();
    }
}
