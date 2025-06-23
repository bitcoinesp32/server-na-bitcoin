from fastapi import FastAPI
import httpx
import asyncio
from contextlib import asynccontextmanager

ceny = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    while True:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=eur")
            if r.status_code == 200:
                data = r.json()
                ceny.update({
                    "bitcoin": float(data["bitcoin"]["eur"]),
                    "ethereum": float(data["ethereum"]["eur"])
                })
        await asyncio.sleep(2)
        yield

app = FastAPI(lifespan=lifespan)

@app.get("/ceny")
async def get_ceny():
    return ceny

# 🔥 Dôležité pre Railway
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
