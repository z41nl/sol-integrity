pragma solidity ^0.8.20;

contract Lottery {
    address public owner;
    address[] public players;
    uint256 public ticketPrice;
    address public lastWinner;

    constructor(uint256 _ticketPrice) {
        owner = msg.sender;
        ticketPrice = _ticketPrice;
    }

    function enter() external payable {
        require(msg.value == ticketPrice);
        players.push(msg.sender);
    }

    function getPlayers() external view returns (address[] memory) {
        return players;
    }

    function balance() external view returns (uint256) {
        return address(this).balance;
    }

    function random() internal view returns (uint256) {
        return uint256(
            keccak256(
                abi.encodePacked(
                    block.prevrandao,
                    block.timestamp,
                    players.length
                )
            )
        );
    }

    function pickWinner() external {
        require(msg.sender == owner);
        require(players.length > 0);

        uint256 index = random() % players.length;

        lastWinner = players[index];

        payable(lastWinner).transfer(address(this).balance);

        delete players;
    }
}
