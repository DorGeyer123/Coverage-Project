import {IFlashLoanReceiver} from './IFlashLoanReceiver.sol';
import {LP_ERC20} from './LP_ERC20.sol';
import {IERC20} from './IERC20.sol';
pragma solidity >=0.8.0;

contract Pool is LP_ERC20 {

  IERC20 public asset;

   

    function deposit(uint256 AmountToMint) public payable returns(uint256) {
      uint256 poolBalance=IERC20(asset).balanceOf(address(this));
      uint256 amount;
        if (totalSupply==0){
            amount=AmountToMint;
        }
        else{
        amount=(AmountToMint*poolBalance)/totalSupply;
        }
        totalSupply+=AmountToMint;
        IERC20(asset).transferFrom(msg.sender,address(this),amount);
        _mint(msg.sender,AmountToMint);
        return amount;

    }

    function withdraw(uint256 amount) public returns (bool success)  {
		_burn(msg.sender,amount);
		IERC20(asset).transferFrom(address(this),msg.sender,amount);
		totalSupply-=amount;
    }

    
    function FlashLoan(address receiverAddress, uint256 amount) public {
            
            uint256 totalPremium = (amount*18)/10000;
            uint256 amountPlusPremium = amount + totalPremium;
            IERC20(asset).transferFrom(address(this),msg.sender,amount);
            require(IFlashLoanReceiver(receiverAddress).executeOperation(amount,totalPremium,msg.sender),'P_INVALID_FLASH_LOAN_EXECUTOR_RETURN');
            IERC20(asset).transferFrom(receiverAddress,address(this),amountPlusPremium);
  }

}
