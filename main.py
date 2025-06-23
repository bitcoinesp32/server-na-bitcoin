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
                        print("Ceny aktualizovane:", ceny)
                    else:
                        print("Chyba HTTP:", r.status_code)
            except Exception as e:
                print("Chyba pri stahovani dat:", e)
            await asyncio.sleep(10)  # aktualizuj kazdych 10s

    task = asyncio.create_task(aktualizuj_ceny())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/ceny")
async def get_ceny():
    return ceny

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mai
