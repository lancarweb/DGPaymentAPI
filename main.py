from fastapi import FastAPI

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
	return {
		"response": True
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
