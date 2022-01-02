certoraRun Pool.sol LP_ERC20.sol IERC20.sol \
    --link Pool:asset=IERC20 \
	--verify Pool:spec.spec \
    --solc solc8.0 \
    --rule $1