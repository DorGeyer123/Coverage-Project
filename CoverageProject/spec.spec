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