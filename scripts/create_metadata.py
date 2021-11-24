from brownie import spartanCollectible, network
from scripts.helpful_scripts import get_RACE, OPENSEA_URL, get_account
from metadata.sample_metadata import metadata_template
from pathlib import Path
import json
import os
from pathlib import Path
import requests

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
# Change this filepath
filepath = "./img/shiba-inu.png"
filename = filepath.split("/")[-1:][0]
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}


def create_metadata():
    spartanContract = spartanCollectible[-1]
    metadata_uri = ""
    ipfs_hash = ""
    number_of_tokens = spartanContract.tokenCounter()
    token_id = number_of_tokens - 1
    if token_id < 0:
        token_id = 0
    print(f"You have created {number_of_tokens} collectibles!")
    RACE = get_RACE(spartanContract.tokenIdToRACE(token_id))
    metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{RACE}.json"
    collectible_metadata = metadata_template
    if Path(metadata_file_name).exists():
        print(f"{metadata_file_name} already exists! Delete it to overwrite")
    else:
        print(f"Creating Metadata file: {metadata_file_name}")
        collectible_metadata["name"] = RACE
        collectible_metadata["description"] = f"An adorable {RACE} pup!"
        image_path = "./img/" + RACE.lower().replace("_", "-") + ".png"

        image_uri = None
        if os.getenv("UPLOAD_PINATA") == "true":
            image_uri, ipfs_hash = UPLOAD_PINATA(image_path)
        image_uri = image_uri if image_uri else "ERROR: NO IMG URI SET"

        collectible_metadata["image"] = image_uri
        with open(metadata_file_name, "w") as file:
            json.dump(collectible_metadata, file)
        if os.getenv("UPLOAD_PINATA") == "true":
            metadata_uri, ipfs_hash = UPLOAD_PINATA(metadata_file_name)
        spartanContract.setTokenURI(token_id, metadata_uri, {"from": get_account()})
        print(
            f"Awesome, you can now view your NFT at {OPENSEA_URL.format(spartanContract.address, spartanContract.tokenCounter() - 1)}"
        )
    return metadata_uri, ipfs_hash


def create_metadata_for_all():
    spartanContract = spartanCollectible[-1]
    metadata_uri = ""
    ipfs_hash = ""
    number_of_tokens = spartanContract.tokenCounter()
    print(f"You have created {number_of_tokens} collectibles!")
    for token_id in range(number_of_tokens):
        RACE = get_RACE(spartanContract.tokenIdToRACE(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{RACE}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = RACE
            collectible_metadata["description"] = f"An adorable {RACE} pup!"
            image_path = "./img/" + RACE.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_PINATA") == "true":
                image_uri = UPLOAD_PINATA(image_path)
            image_uri = image_uri if image_uri else RACE_to_image_uri[RACE]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_PINATA") == "true":
                metadata_uri, ipfs_hash = UPLOAD_PINATA(metadata_file_name)
            print(
                f"Awesome, you can now view your NFT at {OPENSEA_URL.format(ipfs_hash, spartanContract.tokenCounter() - 1)}"
            )
    return metadata_uri, ipfs_hash


# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def UPLOAD_PINATA(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        # "./img/0-PUG.png" -> "0-PUG.png"
        ipfs_hash = response.json()["IpfsHash"]
        image_uri = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        print(image_uri)

        return image_uri, ipfs_hash
