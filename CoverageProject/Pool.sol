import {IFlashLoanReceiver} from './IFlashLoanReceiver.sol';
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
<<<<<<< HEAD

function FlashLoan(address asset, address receiverAddress, uint256 amount) public {
    address receiver = IFlashLoanReceiver(receiverAddress);
    uint256 totalPremium = (amount*18)/10000;
    uint256 amountPlusPremium = amount + totalPremium;
    IERC20(asset).safeTransferFrom(address(this),receiverAddress,amount);
    require(receiver.executeOperation(asset,amount,totalPremium,msg.sender),'P_INVALID_FLASH_LOAN_EXECUTOR_RETURN');
    IERC20(params.asset).safeTransferFrom(receiverAddress,address(this),amountPlusPremium);
  }
 
=======
	
>>>>>>> 4740b133a5921f01b8e808652427afc7a33b26f3
	
	function getEthBalance(address account) public view returns (uint256){
		return account.balance;
	}


}
