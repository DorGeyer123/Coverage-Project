methods
{
     // erc20 function
    balanceOf(address) returns(uint256) envfree
    totalSupply() returns(uint256) envfree
    transfer(address,uint256) returns(bool) envfree
    transferFrom(address,address,uint256) returns(bool) envfree
}


rule sanity(method f){
    calldataarg args;
    env e;
    f(e,args);
    assert false;

}

invariant balance_SE_supply(env e)
    balanceOf(e.msg.sender) <= totalSupply()
    {
        preserved{
            require e.msg.sender != currentContract;
        }
        preserved transfer(address to,uint256 amount){
            require to != e.msg.sender;
        }
        preserved transferFrom(address from, address recipient, uint256 amount){
            require recipient != e.msg.sender;
        }
    }