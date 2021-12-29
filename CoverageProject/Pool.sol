import {IFlashLoanReceiver} from './IFlashLoanReceiver.sol';
pragma solidity >=0.8.0;

contract Pool is LPToken {

    function deposit(address asset, uint256 amount) public payable {
    	IERC20(asset).safeTransferFrom(msg.sender,address(this),amount);
        _mint(msg.sender,amount);
        totalSupply+=amount;
    }

    function withdraw(address asset,uint256 amount) public returns (bool success)  {
		_burn(msg.sender,amount);
		IERC20(asset).safeTransferFrom(address(this),msg.sender,amount);
		totalSupply-=amount;
    }

    
    function FlashLoan(address receiverAddress, uint256 amount) public {
    address receiver = IFlashLoanReceiver(receiverAddress);
    uint256 totalPremium = (amount*18)/10000;
    uint256 amountPlusPremium = amount + totalPremium;
    IERC20(asset).safeTransferFrom(address(this),msg.sender,amount);
    require(receiver.executeOperation(asset,amount,totalPremium,msg.sender),'P_INVALID_FLASH_LOAN_EXECUTOR_RETURN');
    IERC20(asset).safeTransferFrom(receiverAddress,address(this),amountPlusPremium);
  }
 
    function getEthBalance(address account) public view returns (uint256){
		return account.balance;
	}


}
