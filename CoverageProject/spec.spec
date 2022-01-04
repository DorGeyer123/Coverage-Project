using Asset_ERC20 as underlying 
methods
 {
      // pool's erc20 function
     balanceOf(address) returns(uint256) envfree
     totalSupply() returns(uint256) envfree
     transfer(address,uint256) returns(bool) envfree
     transferFrom(address,address,uint256) returns(bool) envfree
     underlying.balanceOf(address) returns(uint256) envfree

     executeOperation(uint256,uint256,address) => DISPATCHER(true)
     transfer(address, uint256) returns (bool) => DISPATCHER(true)
     transferFrom(address, address, uint256) returns (bool) => DISPATCHER(true)
     deposit(uint256) returns(uint256)  => DISPATCHER(true)
     withdraw(uint256) returns (uint256)  => DISPATCHER(true)
     FlashLoan(address, uint256)  => DISPATCHER(true)

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
invariant totalSupply_GE_balance()
    totalSupply() <= underlying.balanceOf(currentContract)
{
        preserved with (env e){
        require e.msg.sender != currentContract;
         }
}

rule deposit_GR_zero(){ //failing due to bugs in the code
    env e;
    require e.msg.sender != currentContract;

    uint256 amount;
    uint256 amountMinted = deposit(e,amount);

    assert amount > 0 <=> amountMinted > 0;
}

rule more_user_shares_less_underlying(method f) // failures need to check
        // filtered {f -> f.selector != transfer(address,uint256).selector && f.selector != transferFrom(address,address,uint256).selector && !f.isView }
        {
    env e;

    uint256 Underlying_balance_before = underlying.balanceOf(e.msg.sender);
    uint256 User_balance_before = balanceOf(e.msg.sender);

    // global_requires(e);

        calldataarg args;
        f(e,args);

    uint256 Underlying_balance_after = underlying.balanceOf(e.msg.sender);
    uint256 User_balance_after = balanceOf(e.msg.sender);

    assert User_balance_after > User_balance_before <=> Underlying_balance_after < Underlying_balance_before;
    assert User_balance_after < User_balance_before <=> Underlying_balance_after > Underlying_balance_before;
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