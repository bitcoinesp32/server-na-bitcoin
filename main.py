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
                    r = await client.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=eur")
                    if r.status_code == 200:
                        ceny.update(r.json())
                        print("Aktualizovane:", ceny)
            except Exception as e:
                print("Chyba pri aktualizacii:", e)
            await asyncio.sleep(10)

    task = asyncio.create_task(aktualizuj_ceny())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/ceny")
async def get_ceny():
    return ceny

# spusti iba lokalne, Railway to ignoruje
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
