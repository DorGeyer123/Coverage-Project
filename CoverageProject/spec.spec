using Asset_ERC20 as underlying
using SymbolicFlashLoanReceiver as flashLoanReceiver

methods
 {
      // pool's erc20 function
     balanceOf(address) returns(uint256) envfree
     totalSupply() returns(uint256) envfree
     underlying.balanceOf(address) returns(uint256) envfree

     executeOperation(uint256,uint256,address) => DISPATCHER(true)
     transfer(address, uint256) returns (bool) => DISPATCHER(true)
     transferFrom(address, address, uint256) returns (bool) => DISPATCHER(true)
     deposit(uint256) returns(uint256)  => DISPATCHER(true)
     withdraw(uint256) returns (uint256)  => DISPATCHER(true)
     FlashLoan(address, uint256)  => DISPATCHER(true)

 }

invariant balance_SE_supply(address user)
     balanceOf(user) <= totalSupply()
     {
         preserved with (env e){
             require e.msg.sender == user;
             require user != currentContract;
         }
         preserved transfer(address to,uint256 amount) with (env e){
             require to != e.msg.sender;
         }
         preserved transferFrom(address from, address recipient, uint256 amount) with (env e){
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
invariant totalSupply_vs_balance()
    totalSupply() == 0 <=> underlying.balanceOf(currentContract) == 0
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

rule user_solvency(address user){
env e;

require user != currentContract && user != flashLoanReceiver.to(e) && user != flashLoanReceiver;
require e.msg.sender != currentContract;

uint256 shares1 = balanceOf(user);
uint256 poolBalance1 = underlying.balanceOf(currentContract);
uint256 supply1 = totalSupply();
require supply1 != 0;
uint256 withdrawableAmount1 = shares1 * poolBalance1 / supply1;
uint256 userBalance1 = underlying.balanceOf(user);
uint256 total_pre = withdrawableAmount1 + userBalance1;

uint256 amount;

FlashLoan(e,flashLoanReceiver, amount);

uint256 shares2 = balanceOf(user);
uint256 poolBalance2 = underlying.balanceOf(currentContract);
uint256 supply2 = totalSupply();
require supply2 != 0;
uint256 withdrawableAmount2 = shares2 * poolBalance2 / supply2;
uint256 userBalance2 = underlying.balanceOf(user);
uint256 total_post = withdrawableAmount2 + userBalance2;

uint256 fee_for_LP = (amount*18*shares2)/(10000 * supply2);
uint256 fee_for_none_LP = (amount*18)/10000 ;

// assert shares1 == shares2;
// assert poolBalance2 > poolBalance1 => f.selector == FlashLoan(address flashLoanReceiver,uint256 amount).selector;
// assert total_post > total_pre =>  total_post - total_pre <= fee  && user!=e.msg.sender;
// assert total_post < total_pre => total_pre - total_post <= fee  && user==e.msg.sender;
assert (user != e.msg.sender && shares1 != 0) => (total_post - total_pre <= fee_for_LP);
// assert user == e.msg.sender && shares1 != 0 =>  total_pre - total_post <= fee_for_LP ;
// assert user != e.msg.sender && shares1 == 0 =>  total_pre == total_post;
// assert user == e.msg.sender && shares1 == 0 =>  total_post + fee_for_none_LP == total_pre;
}
rule user_solvency_without_flashloan(address user, method f)filtered { f-> f.selector != FlashLoan(address,uint256).selector }{
env e;
// require user != e.msg.sender;
require user != currentContract && user != flashLoanReceiver.to(e) ;
global_requires(e);

uint256 shares1 = balanceOf(user);
uint256 poolBalance1 = underlying.balanceOf(currentContract);
uint256 supply1 = totalSupply();
require supply1 != 0;
uint256 withdrawableAmount1 = shares1 * poolBalance1 / supply1;
uint256 userBalance1 = underlying.balanceOf(user);
require withdrawableAmount1 <= to_mathint(2^255) - userBalance1;
uint256 total_pre = withdrawableAmount1 + userBalance1;

address to;
    require user != to;
uint256 amount;

if f.isFallback{}
else
if f.selector == transferFrom(address,address,uint256).selector{
    address from;
    require user != from;
    transferFrom(e,from,to,amount);
    }
else
if f.selector == transfer(address,uint256).selector{
    transfer(e,to,amount);
    }
else
    {
        calldataarg args;
        f(e,args);
    }

uint256 shares2 = balanceOf(user);
uint256 poolBalance2 = underlying.balanceOf(currentContract);
uint256 supply2 = totalSupply();
require supply2 != 0;
uint256 withdrawableAmount2 = shares2 * poolBalance2 / supply2;
uint256 userBalance2 = underlying.balanceOf(user);
// require 2^256 - userBalance2 >= withdrawableAmount2;
require withdrawableAmount2 <= to_mathint(2^255) - userBalance2;
uint256 total_post = withdrawableAmount2 + userBalance2;

assert total_pre == total_post;
}

function global_requires(env e){
    require e.msg.sender != currentContract;
    require e.msg.sender != flashLoanReceiver.to(e);
    require e.msg.sender != flashLoanReceiver;
    requireInvariant totalSupply_vs_balance();
    requireInvariant totalSupply_GE_balance();
}


rule sanity(method f){
    calldataarg args;
    env e;
    f(e,args);
    assert false;

}