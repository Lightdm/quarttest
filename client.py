import aiohttp
from aiohttp import web
import asyncio
import pickle


async def websocket(session):
    async with session.ws_connect('http://localhost:8080/ws') as ws:
        #await ws.send_str('test', compress=None)
        #await ws.send_bytes(pickle.dumps("testbyte"))
        await ws.send_json({ "trig":"time", "val":20})
        async for msg in ws:
            print(pickle.loads(msg.data))
        print("done")
        #await ws.close()
        '''async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await callback(msg.data)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
        '''

async def websocketclockclient(session):
    print("hier")
    async with session.ws_connect('http://localhost:8080/clock') as ws:
        print("auch hier")
        async for msg in ws:
            print(pickle.loads(msg.data))

async def main():
    async with aiohttp.ClientSession() as session:
        await websocket(session)
        #await websocketclockclient(session)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())