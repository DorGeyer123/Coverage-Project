using Asset_ERC20 as underlying 
methods
 {
      // pool's erc20 function
     balanceOf(address) returns(uint256) envfree
     totalSupply() returns(uint256) envfree
     transfer(address,uint256) returns(bool) envfree
     transferFrom(address,address,uint256) returns(bool) envfree
     underlying.balanceOf(address) returns(uint256) envfree
 }

invariant balance_SE_supply(env e)
     balanceOf(e.msg.sender) <= totalSupply()
     {
         preserved with (env e2){
             require e.msg.sender == e2.msg.sender;
             require e2.msg.sender != currentContract;
         }
         preserved transfer(address to,uint256 amount){
             require to != e.msg.sender;
         }
         preserved transferFrom(address from, address recipient, uint256 amount){
             require recipient != e.msg.sender;
         }
     } 

// function global_requires(env e){
//     require e.msg.sender != currentContract;
// }


rule stupid(env e, uint256 x){
    uint256 amount=deposit(e,x);
    assert amount==x;

}
rule sanity(method f){
    calldataarg args;
    env e;
    f(e,args);
    assert false;

}