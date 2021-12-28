
pragma solidity >=0.8.0;
interface IFlashLoanReceiver {
  function executeOperation(assets,amounts,premiums,initiator) external returns (bool){
  }
}