from fastapi import FastAPI, BackgroundTasks
import httpx
import asyncio

app = FastAPI()
ceny = {}

async def aktualizuj_ceny():
    while True:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=eur")
            if r.status_code == 200:
                ceny.update(r.json())
                print("Aktualizovane ceny:", ceny)
        await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(aktualizuj_ceny())

@app.get("/ceny")
async def get_ceny():
    return ceny



