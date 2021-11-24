/* eslint-disable spaced-comment */
/// <reference types="react-scripts" />
import React, { useEffect, useState } from "react"
import eth from "../eth.png"
import dapp from "../dapp.png"
import dai from "../dai.png"
import { YourWallet } from "./yourWallet"
import { TokenFarmContract } from "./tokenFarmContract"
import { useEthers, useContractFunction } from "@usedapp/core"
import { utils, constants } from "ethers"
import spartanCollectible from "../chain-info/spartanCollectible.json"
import { Snackbar, Typography, Button, makeStyles } from "@material-ui/core"
import Alert from "@material-ui/lab/Alert"
import networkMapping from "../chain-info/map.json"
import brownieConfig from "../brownie-config-json.json"
import helperConfig from "../helper-config.json"
import { MintNFT } from "../hooks"
import { Contract } from "@ethersproject/contracts"

export type Token = {
  image: string
  address: string
  name: string
}

// Why not in a css folder? 
// For material UI
// https://material-ui.com/styles/basics/
const useStyles = makeStyles((theme) => ({
  title: {
    color: theme.palette.common.white,
    textAlign: "center",
    padding: theme.spacing(4),
  },
}))

const handleMint = () => {

}
export const Main = () => {
  const { chainId, error } = useEthers()

  const classes = useStyles()
  const networkName = chainId ? helperConfig[chainId] : "ganache"
  console.log(typeof chainId)
  // We need to pull the DAPP token address from the .json file written to by Brownie
  const spartanTokenAddress = chainId ? networkMapping[String(chainId)]["spartanCollectible"][0] : constants.AddressZero
  const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero
  const fauTokenAddress = chainId ? brownieConfig["networks"][networkName]["fau_token"] : constants.AddressZero


  const { abi } = spartanCollectible
  const tokenFarmContractAddress = chainId ? networkMapping[String(chainId)]["spartanCollectible"][0] : constants.AddressZero

  const tokenFarmInterface = new utils.Interface(abi)

  const tokenFarmContract = new Contract(
    tokenFarmContractAddress,
    tokenFarmInterface
  )


  console.log("Here " + useContractFunction(tokenFarmContract, "safeMint", { transactionName: "Approve ERC721 transfer", }))
  // console.log(dappTokenAddress)
  /**
   * Our single central location to store info on support tokens.
   * This is the only place you'll need to add a new token to get it to display in the UI!
   * 
   * Modularize the addresses like with `dappTokenAddress`
   * To make it chain agnostic
   */
  const supportedTokens: Array<Token> = [
    {
      image: eth,
      address: wethTokenAddress,
      name: "WETH",
    },
    {
      image: dai,
      address: fauTokenAddress,
      name: "FAU",
    }
  ]

  const [showNetworkError, setShowNetworkError] = useState(false)

  const handleCloseNetworkError = (
    event: React.SyntheticEvent | React.MouseEvent,
    reason?: string
  ) => {
    if (reason === "clickaway") {
      return
    }

    showNetworkError && setShowNetworkError(false)
  }

  /**
   * useEthers will return a populated 'error' field when something has gone wrong.
   * We can inspect the name of this error and conditionally show a notification
   * that the user is connected to the wrong network.
   */
  useEffect(() => {
    if (error && error.name === "UnsupportedChainIdError") {
      !showNetworkError && setShowNetworkError(true)
    } else {
      showNetworkError && setShowNetworkError(false)
    }
  }, [error, showNetworkError])

  // function handleMint mints a NFT token and returns the OpenSea address



  return (
    <>
      <Typography
        variant="h2"
        component="h1"
        classes={{
          root: classes.title,
        }}
      >
        Token Farm
      </Typography>
      <Button color="primary"
        variant="contained"
        size="large"
        onClick={handleMint}> Button</Button>
      <YourWallet supportedTokens={supportedTokens} />
      <TokenFarmContract supportedTokens={supportedTokens} />
      <Snackbar
        open={showNetworkError}
        autoHideDuration={5000}
        onClose={handleCloseNetworkError}
      >
        <Alert onClose={handleCloseNetworkError} severity="warning">
          You gotta connect to the Kovan or Rinkeby network!
        </Alert>
      </Snackbar>
    </>
  )
}
