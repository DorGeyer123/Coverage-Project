certoraRun Pool.sol Asset_ERC20.sol SymbolicFlashLoanReceiver.sol \
    --link Pool:asset=Asset_ERC20 \
	--verify Pool:spec.spec \
    --solc solc8.0 \
    --staging \
    --rule $1
#    --toolOutput ../output \