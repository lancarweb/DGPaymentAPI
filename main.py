# web3py
import json
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

# FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

import requests

# load .env
import os
from dotenv import load_dotenv
load_dotenv()

# profiders
infura_url = "https://mainnet.infura.io/v3/06b3b50902f34272b0c1a09a08a71f18" # dgp
web3 = Web3(Web3.HTTPProvider(infura_url))

# connection
print("Connection provider : %s" % web3.isConnected())

# contract ABI DGP
abi = json.loads(os.getenv("ABI"))

# address DGP
address = "0x927159670C50042109d7C0f4aEd0Cee89452433E"

# contract DGP
contract = web3.eth.contract(address=address, abi=abi)

desc = """
This API reference includes all technical documentation developers need to integrate third-party applications and platforms.
"""

tags_metadata = [
			{
			"name": "root",
			"description": "Root response"

		},
			{
			"name": "info",
			"description": "This operation is used to get DGP info Totalsupply, Name, Symbol"
		},
			{
			"name": "balance",
			"description": "This operation is used to get DGP Balance from Address or Token"
		},
			{
			"name": "receipt",
			"description": "This operation is used to get receipt information from Transaction Hash"
		},
			{
			"name": "transfer",
			"description": "This operation is used to send funds. between a dgp token to another dgp token."
		},
			{
			"name": "conversion",
			"description": "This operation is used to convert dgp to other currencies, currently only USD and IDR are supported."
		},
			{
			"name": "create",
			"description": "This operation is used to create a wallet. with easy steps just send random word."
		}
	]

# field_check_address
class Address(BaseModel):
	address: str

# field_check_tx_hash
class Txhash(BaseModel):
	tx_hash: str

# field_transfer
class Transfer(BaseModel):
	address_from: str
	address_to: str
	value: str
	private_key: str
	
# price-conversion
class Priceconversion(BaseModel):
	currency: str
	amount: str

# create-account
class CreateAccount(BaseModel):
	crypt_security: str

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
	redoc_url=None,
	openapi_tags=tags_metadata
	)

@app.get("/", tags=["root"])
async def root():
	return {
		"response": True
	}

@app.get("/api/dgp", tags=["info"])
async def dgp_api():
	totalSupply = contract.functions.totalSupply().call()

	return {
		"totalsupply": str(web3.fromWei(totalSupply, 'ether')),
		"name": contract.functions.name().call(),
		"symbol": contract.functions.symbol().call()
	}

@app.post("/api/dgp/v1/balance", tags=["balance"])
async def dgp_balance(addrs: Address):
	balance = contract.functions.balanceOf(Web3.toChecksumAddress(addrs.address)).call()
	balance_from_wei = web3.fromWei(balance, 'ether')
	return {
		"balance": balance_from_wei
	}

@app.post("/api/dgp/v1/receipt", tags=["receipt"])
async def dgp_receipt(tx: Txhash):
	receipt = web3.eth.get_transaction_receipt(tx.tx_hash)
	# print(web3.eth.getTransaction(tx.tx_hash))
	txhash_json_value = json.loads(Web3.toJSON(receipt))
	return {
		"transaction_details": txhash_json_value
	}

@app.post("/api/dgp/v1/transfer", tags=["transfer"])
async def dgp_transfer(trf: Transfer):
	addr_from = trf.address_from
	addr_to = trf.address_to
	value = trf.value
	pkey = trf.private_key
	
	transaction = contract.functions.transfer(str(addr_to), web3.toWei(str(value), 'ether')).buildTransaction({
		'chainId': web3.eth.chain_id,
		'gas': 70000,
		'gasPrice': web3.eth.gas_price,
		# 'gasPrice': web3.toWei('40', 'gwei'),
		# 'gasPrice': web3.eth.max_priority_fee,
		'nonce': web3.eth.getTransactionCount(str(addr_from)) #my.account
	})

	signed_txn = web3.eth.account.signTransaction(transaction, str(pkey)) #private.key
	txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
	txn_to_hex = web3.toHex(txn_hash)	

	return {
		"txn_hash_status": txn_to_hex
	}

@app.post("/api/dgp/v1/price-conversion", tags=["conversion"])
async def dgp_price_conversion(conv: Priceconversion):	
	currency = conv.currency
	amount = conv.amount
		
	s = requests.session()
	
	if 'idr' == currency:
		data = s.get('https://api.coinmarketcap.com/data-api/v3/tools/price-conversion?amount=1&convert_id=2794&id=7864')
		data_ = data.json()['data']['quote'][0]['price']
		data__ = data_ * int(amount)
		
		return {
			"currency": "IDR",
			"result": str(data__)
		}

	elif 'usd' == currency:
		data = s.get('https://api.coinmarketcap.com/data-api/v3/tools/price-conversion?amount=1&convert_id=2781&id=7864')
		data_ = data.json()['data']['quote'][0]['price']
		data__ = data_ * int(amount)
		
		return {
			"currency": 'USD',
			"result": str(data__)
		}
	
	else:
		return {"message": "currency_error"}

@app.post("/api/dgp/v1/create", tags=["create"])
async def create(sc: CreateAccount):
	account = web3.eth.account.create(sc.crypt_security)
	
	return {
		"address": account._address,
		"private_key": account._private_key.hex()
	}
