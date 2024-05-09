const FlexCoin = artifacts.require("FlexCoin");
const Duration = artifacts.require('Duration');
const DurationSecure = artifacts.require('DurationSecure');
const FutureBlock = artifacts.require('FutureBlock');
const RealTime = artifacts.require('RealTime');

module.exports = function (deployer) {
  deployer.deploy(FlexCoin, 'Deploy flexcoin!');
  deployer.deploy(Duration, 'Deploy duration!');
  deployer.deploy(DurationSecure, 'Deploy duration secure!');
  deployer.deploy(FutureBlock, 'Deploy future block!');
  deployer.deploy(RealTime, 'Deploy real time!');
};

