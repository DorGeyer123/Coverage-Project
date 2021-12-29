
pragma solidity >=0.8.0;
interface IFlashLoanReceiver {
  function executeOperation(address asset,uint256 amount,uint256 premium,address initiator) external returns (bool);
}
