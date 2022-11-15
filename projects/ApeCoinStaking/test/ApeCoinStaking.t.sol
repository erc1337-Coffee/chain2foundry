// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.10;

import "forge-std/Test.sol";
import "../src/ApeCoinStaking.sol";

contract ApeCoinStakingTest is Test {
    ApeCoinStaking public my_contract;
    function setUp() public {
       my_contract = new ApeCoinStaking();
    }
}
		