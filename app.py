from fastapi import FastAPI
from pyquotex.stable_api import Quotex

app = FastAPI()

EMAIL = "xiwili9878@cucadas.com"
PASSWORD = "Addy1122"

@app.get("/")
def root():
    return {"status": "ok", "service": "quotex-render"}

@app.get("/candle")
async def candle():
    client = Quotex(email=EMAIL, password=PASSWORD, lang="en")

    await client.connect()
    data = await client.get_candle("BTCUSD", 60, 1)
    await client.close()

    return data[0]
