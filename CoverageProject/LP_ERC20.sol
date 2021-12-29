pragma solidity >=0.8.0;
contract LP_ERC20 {

    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transfer(address recipient, uint256 amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        unchecked {
            balanceOf[recipient] += amount;
        }
        return true;
    }

    function transferFrom(address from,address recipient,uint256 amount) 
    external returns (bool) {
        if (allowance[from][msg.sender] != type(uint256).max) {
            allowance[from][msg.sender] -= amount;}
        balanceOf[from] -= amount;
        unchecked {
            balanceOf[recipient] += amount;
        }
        return true;
    }

    function _mint(address recipient, uint256 amount) internal {
        totalSupply += amount;
        unchecked {
            balanceOf[recipient] += amount;
        }  
    }

    function _burn(address from, uint256 amount) internal {
        balanceOf[from] -= amount;
        unchecked {
            totalSupply -= amount;
        }
    }
     


}
