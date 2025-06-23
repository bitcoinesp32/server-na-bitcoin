from fastapi import FastAPI
import httpx
import asyncio
from contextlib import asynccontextmanager

ceny = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    async def aktualizuj_ceny():
        while True:
            try:
                async with httpx.AsyncClient() as client:
                    btc_r = await client.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR")
                    eth_r = await client.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHEUR")

                    if btc_r.status_code == 200 and eth_r.status_code == 200:
                        btc = float(btc_r.json()["price"])
                        eth = float(eth_r.json()["price"])

                        ceny.update({
                            "bitcoin": {"eur": round(btc, 2)},
                            "ethereum": {"eur": round(eth, 2)}
                        })
                        print("Aktualizovane:", ceny)
            except Exception as e:
                print("Chyba:", e)
            await asyncio.sleep(1)  # ⏱ každú sekundu!

    task = asyncio.create_task(aktualizuj_ceny())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/ceny")
async def get_ceny():
    return ceny

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

