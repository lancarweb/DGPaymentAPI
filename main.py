# web3py
import json
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

# FastAPI
from fastapi import FastAPI

# load .env
import os
from dotenv import load_dotenv
load_dotenv()

# profiders
infura_url = "https://mainnet.infura.io/v3/06b3b50902f34272b0c1a09a08a71f18" # dgp
web3 = Web3(Web3.HTTPProvider(infura_url))

# contract ABI DGP
abi = json.loads(os.getenv("ABI"))

# address DGP
address = "0x927159670C50042109d7C0f4aEd0Cee89452433E"

# contract DGP
contract = web3.eth.contract(address=address, abi=abi)

desc = """
This API reference includes all technical documentation developers need to integrate third-party applications and platforms.
"""

app = FastAPI(
	title="DGPaymentAPI",
	description=desc,
	version="1.0",
	terms_of_service="https://dgpaytech.com/terms",
	contact={
		"name": "DGPaymentAPI Token",
		"url": "https://dgpaytech.com",
		"email": "support@dgpaytech.com"
	},
	license_info={
		"name": "License",
		"url": "https://api.dgpaytech.com"
	},
	docs_url="/documentation",
	redoc_url=None
	)

@app.get("/")
async def root():
	return {
		"response": True
	}

@app.get("/api/dgp")
async def dgp_api():
	totalSupply = contract.functions.totalSupply().call()

	return {
		"totalsupply": str(web3.fromWei(totalSupply, 'ether')),
		"name": contract.functions.name().call(),
		"symbol": contract.functions.symbol().call()
	}

@app.get("/api/dgp/v1/balance")
async def dgp_balance():
	return {
		"response": True
	}

@app.get("/api/dgp/v1/receipt")
async def dgp_receipt():
	return {
		"response": True
	}

@app.get("/api/dgp/v1/transfer")
async def dgp_transfer():
	return {
		"response": True
	}

@app.get("/api/dgp/v1/price-conversion")
async def dgp_price_conversion():
	return {
		"response": True
	}

@app.get("/api/dgp/v1/wallet")
async def wallet():
	return {
		"response": True
	}
