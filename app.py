from fastapi import FastAPI
from pyquotex.stable_api import Quotex

app = FastAPI()

EMAIL = "xiwili9878@cucadas.com"
PASSWORD = "Addy1122"

def analyze_candle(c):
    open_ = c["open"]
    close = c["close"]
    high = c["high"]
    low = c["low"]

    body = abs(close - open_)
    upper_wick = high - max(open_, close)
    lower_wick = min(open_, close) - low

    color = "green" if close > open_ else "red"

    return {
        "open": open_,
        "close": close,
        "high": high,
        "low": low,
        "color": color,
        "body": round(body, 5),
        "upper_wick": round(upper_wick, 5),
        "lower_wick": round(lower_wick, 5)
    }


@app.get("/multi-candle")
async def multi_candle(pairs: str):
    """
    Example:
    /multi-candle?pairs=BTCUSD,ETHUSD
    """

    pair_list = pairs.upper().split(",")[:5]

    client = Quotex(email=EMAIL, password=PASSWORD, lang="en")
    await client.connect()

    result = {}

    for pair in pair_list:
        candles = await client.get_candle(pair, 60, 2)
        closed_candle = candles[-2]  # ✅ CLOSED candle only
        result[pair] = analyze_candle(closed_candle)

    await client.close()
    return result
