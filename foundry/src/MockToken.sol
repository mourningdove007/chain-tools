// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract MockERC20 {
    mapping(address => mapping(address => uint256)) private _allowances;
    mapping(address => uint256) public balances;

    string public name;
    string public symbol;
    uint8 public decimals = 18;

    constructor(string memory _name, string memory _symbol) {
        name = _name;
        symbol = _symbol;
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        _allowances[msg.sender][spender] = amount;
        return true;
    }

    function allowance(
        address owner,
        address spender
    ) public view returns (uint256) {
        return _allowances[owner][spender];
    }

    function totalSupply() public pure returns (uint256) {
        return 0;
    }

    function transfer()
        public
        pure
        returns (
            // address recipient,
            // uint256 amount
            bool
        )
    {
        return false;
    }
    function transferFrom()
        public
        pure
        returns (
            // address sender,
            // address recipient,
            // uint256 amount
            bool
        )
    {
        return false;
    }
    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function balanceOf(address account) external view returns (uint256) {
        return balances[account];
    }
}
