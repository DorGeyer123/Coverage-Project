certoraRun Pool.sol Asset_ERC20.sol SymbolicFlashLoanReceiver.sol \
    --link Pool:asset=Asset_ERC20 \
	--verify Pool:spec.spec \
    --solc solc8.0 \
    --staging \
    --cache AbstractPool \
    --msg "Abstract Pool with flash loan \n $1 $2" \
    --rule $1
#    --toolOutput ../output \