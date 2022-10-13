from multiprocessing.connection import wait
import aiohttp
from aiohttp import web
import pickle
import time
import weakref
import asyncio
import datetime
import json


def get_clock():
    t = (datetime.datetime.now()-tzero).total_seconds()
    t = t % 60
    return t

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)

    msg = await ws.receive()

    print(msg.type)
    data = json.loads(msg.data)
    print(data)

    print(data["trig"])


    sent_val = data["val"]

    try:
        match data["trig"]:
            case "int":
                while True:
                    await asyncio.sleep(sent_val)
                    t = round(get_clock(),1)
                    await ws.send_bytes(pickle.dumps(t))
                    print(t)
            case "time":
                t = get_clock()
                dt = sent_val - t
                if dt <= 0:
                    dt += 60
                await asyncio.sleep(dt)
                t = round(get_clock(),1)
                await ws.send_bytes(pickle.dumps(t))
                while True:
                    await asyncio.sleep(60)
                    t = round(get_clock(),1)
                    await ws.send_bytes(pickle.dumps(t))
            case _:
                print("trig fehler")
            

            
        
    finally:
        request.app['websockets'].discard(ws)
        print('websocket connection closed')
        return ws

tzero = datetime.datetime.now()


app = web.Application()
app['websockets'] = weakref.WeakSet()

app.add_routes([web.get('/ws', websocket_handler)])


web.run_app(app)
