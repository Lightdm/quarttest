from quart import Quart, render_template, websocket, request, jsonify

app = Quart(__name__)

@app.route("/")
async def hello():
    return await render_template("index.html")

@app.post("/api")
async def json():
    print(request.is_json, request.mimetype)
    data = await request.get_json()
    return {"input": data, "extra": True}

@app.websocket("/ws")
async def ws():
    while True:
        await websocket.send("hello")
        await websocket.send_json({"hello": "world"})

if __name__ == "__main__":
    app.run()