import {IFlashLoanReceiver} from './IFlashLoanReceiver.sol';
import {ERC20} from './ERC20.sol';
import {IERC20} from './IERC20.sol';
pragma solidity >=0.8.0;

contract Pool is ERC20 {

IERC20 public asset;   

    function deposit(uint256 amount) public payable returns(uint256 shares) {
      uint256 poolBalance=asset.balanceOf(address(this));
        if (totalSupply()==0){
            shares = amount;
        }
        else{
        shares = ( amount * totalSupply() ) / poolBalance;
        require (shares != 0);
        amount = (shares*poolBalance)/totalSupply(); //the minimal amount required given the AmountToMint
        require (amount != 0);
        }
        // totalSupply+=AmountToMint;
        asset.transferFrom(msg.sender,address(this),amount);
        _mint(msg.sender,shares);
    }

    function withdraw(uint256 shares) public returns (uint256 amountOut)  {
    uint256 poolBalance=asset.balanceOf(address(this));
    amountOut = shares * poolBalance / totalSupply();
    require (amountOut != 0);
    shares = amountOut * totalSupply() / poolBalance;
    require (shares != 0);
		_burn(msg.sender,shares);
		asset.transferFrom(address(this),msg.sender,amountOut);
    }

    
    function FlashLoan(address receiverAddress, uint256 amount) public {
            
    uint256 totalPremium = (amount*18)/10000;
    uint256 amountPlusPremium = amount + totalPremium;
    asset.transferFrom(address(this),msg.sender,amount);
    require(IFlashLoanReceiver(receiverAddress).executeOperation(amount,totalPremium,msg.sender),'P_INVALID_FLASH_LOAN_EXECUTOR_RETURN');
    asset.transferFrom(receiverAddress,address(this),amountPlusPremium);
  }

}
