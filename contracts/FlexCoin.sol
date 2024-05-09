
pragma solidity ^0.4.11;




contract FlexCoin {

    struct House {
        address owner;
        address smartMeter;
        uint flexCoinBalance;
    }

    mapping(address => House) houses;
    uint public numHouses;

    event Transfer(address from, address to, uint flexCoinAmount);
    event smartMeterPlan(address buyerFlex, address smartMeter, int flexAmount, uint[] interval);


    function newHouse() payable public {
        numHouses = numHouses + 1;
        House h = houses[msg.sender];
        h.smartMeter = msg.sender;
        h.flexCoinBalance = 200000000000;
    }


    function getHouse(address _address) public constant returns (address, uint) {
        return (houses[_address].smartMeter, houses[_address].flexCoinBalance);
    }

    function transferHouse(address _from, address _to, uint _amount){
        require(houses[_from].flexCoinBalance >= _amount);
        require(houses[_to].flexCoinBalance + _amount >= houses[_to].flexCoinBalance);
        houses[_from].flexCoinBalance -= _amount;
        houses[_to].flexCoinBalance += _amount;
        Transfer(_from, _to, _amount);
    }


}
