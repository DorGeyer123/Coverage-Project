import {LPToken} from './LPToken.sol';
pragma solidity >=0.8.0;

contract Pool is LPToken {

    function deposit() public payable {
        _mint(msg.sender,msg.value);
        totalSupply+=msg.value;
    }

    function withdraw(uint256 amount) public returns (bool success)  {
		_burn(msg.sender,amount);
		success = payable(msg.sender).send(amount);
		totalSupply-=amount;
    }
	
	
	function getEthBalance(address account) public view returns (uint256){
		return account.balance;
	}
}
