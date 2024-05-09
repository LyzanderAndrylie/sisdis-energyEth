pragma solidity ^0.4.11;
import "./FlexCoin.sol";

contract FutureBlock{





    struct Offer {
        address owner;
        int offerAmount;
        uint[2] interval;
        uint offerNr;

        mapping(uint => Bid) acceptedBids;
        uint numAcceptedBids;
        uint acceptedPrice;
        bool fulfilled;
    }


    struct Bid {
        address bidder;
        uint offerNr;
        uint bidNr;
        int bidAmount;
        uint bidPrice;
    }

    mapping(uint => Offer) public offers;
    mapping(uint => Bid) public bids;
    uint public numOffers;
    uint public numBids;



    event NewOffer();
    event UpdateBid();
    event CorrectionOffer();



    function newOffer(int _amount, uint _startInterval, uint _endInterval) public {
        NewOffer;
        numOffers = numOffers + 1;
        Offer o = offers[numOffers];
        o.offerNr = numOffers;
        o.owner = msg.sender;
        o.offerAmount = _amount;
        o.interval[0] = _startInterval;
        o.interval[1] = _endInterval;
        o.fulfilled = false;
    }

    function getOffer(uint _offerNr) public constant returns(address, int, uint, uint, bool) {
        return(offers[_offerNr].owner, offers[_offerNr].offerAmount, offers[_offerNr].interval[0], offers[_offerNr].acceptedPrice, offers[_offerNr].fulfilled);
    }

    function setBid(uint _offerNr, int _bidAmount, uint _bidPrice) public returns(bool success)  {
        if (offers[_offerNr].fulfilled == true) {  return false;  }

        numBids = numBids + 1;
        Bid b = bids[numBids];
        b.bidder = msg.sender;
        b.offerNr = _offerNr;
        b.bidNr = numBids;
        b.bidAmount = _bidAmount;
        b.bidPrice = _bidPrice;
        return true;
    }

    function updateBid(uint _offerNr, uint _bidNr, int _bidAmount, uint _bidPrice) public returns(bool success)  {

        UpdateBid;
        if (offers[_offerNr].fulfilled == true) {  return false;  }
        if(bids[_bidNr].bidder == msg.sender && bids[_bidNr].offerNr == _offerNr){

            bids[_bidNr].bidAmount = _bidAmount;
            bids[_bidNr].bidPrice = _bidPrice;
            return true;
        }
        else{
            return false;
        }
    }

    function getBid(uint _bidNr) public constant returns(address, int, uint){

        return(bids[_bidNr].bidder, bids[_bidNr].bidAmount, bids[_bidNr].bidPrice);
    }



    function setAcceptedBids(uint _offerNr, uint _bidNr) public {
        require(offers[_offerNr].owner == msg.sender);
        offers[_offerNr].acceptedBids[offers[_offerNr].numAcceptedBids] = bids[_bidNr];
        offers[_offerNr].numAcceptedBids = offers[_offerNr].numAcceptedBids + 1;
    }

    function setAcceptedPrice(uint _offerNr, uint _acceptedPrice) {
        require(offers[_offerNr].owner == msg.sender);
        offers[_offerNr].acceptedPrice = _acceptedPrice;
    }

    function transferAndClose(uint _offerNr, address contractAddress) public returns (bool success){

        require(offers[_offerNr].owner == msg.sender);
        uint i = 0;
        FlexCoin f = FlexCoin(contractAddress);

        if (offers[_offerNr].offerAmount < 0) {


            for (i; i < offers[_offerNr].numAcceptedBids; i++) {
                if (offers[_offerNr].acceptedBids[i].bidPrice <= offers[_offerNr].acceptedPrice) {
                    f.transferHouse(offers[_offerNr].owner, offers[_offerNr].acceptedBids[i].bidder, uint(-offers[_offerNr].acceptedBids[i].bidAmount) * offers[_offerNr].acceptedPrice);
                }
            }
        }
        if (offers[_offerNr].offerAmount > 0) {
            for (i; i < offers[_offerNr].numAcceptedBids; i++) {
                if (offers[_offerNr].acceptedBids[i].bidPrice >= offers[_offerNr].acceptedPrice) {
                    f.transferHouse(offers[_offerNr].acceptedBids[i].bidder, offers[_offerNr].owner, uint(offers[_offerNr].acceptedBids[i].bidAmount) * offers[_offerNr].acceptedPrice);
                }
            }
        }
        if (true){
            offers[_offerNr].fulfilled = true;
        }
        return(true);
    }
}
