import aiohttp
from aiohttp import web
import asyncio
import pickle


async def websocket(session):
    async with session.ws_connect('http://localhost:8080/ws') as ws:
        await ws.send_json({ "trig":"int", "val":1})
        async for msg in ws:
            print(pickle.loads(msg.data))
        print("done")


async def main():
    async with aiohttp.ClientSession() as session:
        await websocket(session)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
