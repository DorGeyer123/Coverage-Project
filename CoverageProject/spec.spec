using Asset_ERC20 as underlying
using SymbolicFlashLoanReceiver as flashLoanReceiver

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
        filtered {f -> f.selector != transfer(address,uint256).selector && f.selector != transferFrom(address,address,uint256).selector && !f.isView }
        {
    env e;

    uint256 Underlying_balance_before = underlying.balanceOf(e.msg.sender);
    uint256 User_balance_before = balanceOf(e.msg.sender);

    global_requires(e);

        calldataarg args;
        f(e,args);

    uint256 Underlying_balance_after = underlying.balanceOf(e.msg.sender);
    uint256 User_balance_after = balanceOf(e.msg.sender);

    assert User_balance_after > User_balance_before <=> Underlying_balance_after < Underlying_balance_before;
    assert User_balance_after < User_balance_before <=> Underlying_balance_after > Underlying_balance_before;
}

rule more_shares_more_withdraw(){ //failing
    env e;

    uint256 sharesX;
    uint256 sharesY;
    uint256 amountX;
    uint256 amountY;

    global_requires(e);

    storage init = lastStorage;

    amountX =  withdraw(e,sharesX);
    amountY =  withdraw(e,sharesY) at init;

    assert sharesX > sharesY => amountX >= amountY;
}

rule flashLoan_adds_value(address receiver, uint256 amount){
    env e;

    global_requires(e);
    uint256 totalSupply_pre = totalSupply();
    // require totalSupply_pre != 0;
    uint256 balance_pre = underlying.balanceOf(currentContract);
    require balance_pre == 2 * totalSupply_pre;
    FlashLoan(e,receiver,amount);
    uint256 totalSupply_post = totalSupply();
    // require totalSupply_post != 0;
    uint256 balance_post = underlying.balanceOf(currentContract);
    
    assert flashLoanReceiver.callBackOption(e) == 0 => balance_post > balance_pre;
    //assert balance_post/totalSupply_post >= balance_pre/totalSupply_pre;
    assert balance_post * totalSupply_pre >= balance_pre * totalSupply_post;
}

rule user_solvency(address user, method f){
env e;
require user != e.msg.sender;
require user != currentContract && user != flashLoanReceiver.to(e) && user != flashLoanReceiver;

uint256 shares1 = balanceOf(user);
uint256 poolBalance1 = underlying.balanceOf(currentContract);
uint256 supply1 = totalSupply();
require supply1 != 0;
uint256 withdrawableAmount1 = shares1 * poolBalance1 / supply1;
uint256 userBalance1 = underlying.balanceOf(user);
uint256 total_pre = withdrawableAmount1 + userBalance1;

        calldataarg args;
        f(e,args);

uint256 shares2 = balanceOf(user);
uint256 poolBalance2 = underlying.balanceOf(currentContract);
uint256 supply2 = totalSupply();
require supply2 != 0;
uint256 withdrawableAmount2 = shares2 * poolBalance2 / supply2;
uint256 userBalance2 = underlying.balanceOf(user);
uint256 total_post = withdrawableAmount1 + userBalance2;

uint256 amount;
uint256 fee = (amount*18)/10000;

// assert poolBalance2 > poolBalance1 => f.selector == FlashLoan(address flashLoanReceiver,uint256 amount).selector;
assert total_post > total_pre => ( f.selector == FlashLoan(address flashLoanReceiver,uint256 amount).selector &&
                                   total_post - total_pre <= fee  && user!=e.msg.sender;
assert total_post < total_pre => ( f.selector == FlashLoan(address flashLoanReceiver,uint256 amount).selector &&
                                   total_pre - total_post <= fee  && user==e.msg.sender;

}

function global_requires(env e){
    require e.msg.sender != currentContract;
    require e.msg.sender != flashLoanReceiver.to(e);
    require e.msg.sender != flashLoanReceiver;
}


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