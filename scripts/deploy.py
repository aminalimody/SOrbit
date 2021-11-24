from brownie import spartanCollectible, TokenFarm, network, config
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
)
import shutil
import os
import yaml
import json
from web3 import Web3
from scripts.create_metadata import create_metadata

KEPT_BALANCE = Web3.toWei(100, "ether")

sample_token_uri = "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=0-shiba-inu.json"


def deploy_token_farm_and_spartan_token(update_front_end_flag=False):
    account = get_account()
    spartanToken = spartanCollectible.deploy(
        {"from": account},
    )
    token_farm = TokenFarm.deploy(
        spartanToken.address,
        {"from": account},
        # publish_source=config["networks"][network.show_active()]["verify"],
    )

    # fau_token = get_contract("fau_token")
    # weth_token = get_contract("weth_token")

    # add_allowed_tokens(
    #     token_farm,
    # {
    # dapp_token: get_contract("dai_usd_price_feed"),
    # fau_token: get_contract("dai_usd_price_feed"),
    #        weth_token: get_contract("eth_usd_price_feed"),
    #  },
    #   account,
    # )
    if update_front_end_flag:
        update_front_end()
    return token_farm, spartanToken


def add_allowed_tokens(token_farm, dict_of_allowed_token, account):
    for token in dict_of_allowed_token:
        token_farm.addAllowedTokens(token.address, {"from": account})
        tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_token[token], {"from": account}
        )
        tx.wait(1)
    return token_farm


def update_front_end():
    print("Updating front end...")
    # The Build
    copy_folders_to_front_end("./build/contracts", "./front_end/src/chain-info")

    # The Contracts
    copy_folders_to_front_end("./contracts", "./front_end/src/contracts")

    # The ERC20
    copy_files_to_front_end(
        "./build/contracts/dependencies/OpenZeppelin/openzeppelin-contracts@4.3.2/ERC20.json",
        "./front_end/src/chain-info/ERC20.json",
    )
    # The ERC721
    copy_files_to_front_end(
        "./build/contracts/dependencies/OpenZeppelin/openzeppelin-contracts@4.3.2/ERC721.json",
        "./front_end/src/chain-info/ERC721.json",
    )
    # The Map
    copy_files_to_front_end(
        "./build/deployments/map.json",
        "./front_end/src/chain-info/map.json",
    )

    # The Config, converted from YAML to JSON
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open(
            "./front_end/src/brownie-config-json.json", "w"
        ) as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print("Front end updated!")


def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def copy_files_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copyfile(src, dest)


# function to mint NFT
def mint_collectible(_raceId):
    account = get_account()
    spartanContract = spartanCollectible[-1]
    tokenFarm = TokenFarm[-1]
    # fund_with_link(tokenFarm.address, amount=Web3.toWei(0.1, "ether"))
    # newCollectible = spartanContract.safeMint(        account, tokenId + 1, metadata_uri, {"from": account}    )
    newCollectible = spartanContract.safeMint(account, _raceId, {"from": account})
    newCollectible.wait(1)
    print("Collectible created!")


def main():
    # deploy_token_farm_and_spartan_token(update_front_end_flag=True)
    mint_collectible(2)
    metadata_uri, ipfs_hash = create_metadata()
    # account = get_account()
    # spartanContract = spartanCollectible[-1]
    # print(spartanContract.tokenURI(0))
