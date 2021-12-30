import {IFlashLoanReceiver} from './IFlashLoanReceiver.sol';
import {LP_ERC20} from './LP_ERC20.sol';
import {IERC20} from './IERC20.sol';
pragma solidity >=0.8.0;

contract Pool is LP_ERC20 {

    function deposit(address asset, uint256 amount) public payable {
    	IERC20(asset).transferFrom(msg.sender,address(this),amount);
      uint256 poolBalance=IERC20(asset).balanceOf(address(this));
      uint256 AmountToMint;
        
        if (totalSupply==0){
            AmountToMint=amount;
            _mint(msg.sender,amount);
        }
        else{
        AmountToMint= (amount*totalSupply)/poolBalance;
        _mint(msg.sender,AmountToMint);
        }
        totalSupply+=AmountToMint;
    }

    function withdraw(address asset,uint256 amount) public returns (bool success)  {
		_burn(msg.sender,amount);
		IERC20(asset).transferFrom(address(this),msg.sender,amount);
		totalSupply-=amount;
    }

    
    function FlashLoan(address asset,address receiverAddress, uint256 amount) public {
            
            uint256 totalPremium = (amount*18)/10000;
            uint256 amountPlusPremium = amount + totalPremium;
            IERC20(asset).transferFrom(address(this),msg.sender,amount);
            require(IFlashLoanReceiver(receiverAddress).executeOperation(asset,amount,totalPremium,msg.sender),'P_INVALID_FLASH_LOAN_EXECUTOR_RETURN');
            IERC20(asset).transferFrom(receiverAddress,address(this),amountPlusPremium);
  }

}
