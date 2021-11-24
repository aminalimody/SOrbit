// An NFT Contract
// Where the tokenURI can be one of 3 different dogs
// Randomly selected

// SPDX-License-Identifier: MIT
pragma solidity >0.6.6;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract spartanCollectible is ERC721URIStorage {
    constructor() public ERC721("Spartans", "SPTA") {}

    uint256 public tokenCounter;
    enum RACE {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => RACE) public tokenIdToRACE;
    event RACEAssigned(uint256 indexed tokenId, RACE race);

    function safeMint(address owner, uint256 raceId) public {
        RACE race = RACE(raceId % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToRACE[newTokenId] = race;
        emit RACEAssigned(newTokenId, race);
        address owner = msg.sender;
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory tokenURI) public {
        // pug, shiba inu, st bernard
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner no approved"
        );
        _setTokenURI(tokenId, tokenURI);
    }
}
