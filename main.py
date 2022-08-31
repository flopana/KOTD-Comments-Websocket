import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

import db
from Listener import Listener

global_listener = Listener()
commentsToSend = []

app = FastAPI()
conn = None
cursor = None


@app.on_event("startup")
async def startup_event():
    global conn, cursor
    conn = db.conn
    cursor = db.cursor
    await global_listener.start_listening()


@app.on_event("shutdown")
async def shutdown_event():
    global conn
    conn.close()
    await global_listener.stop_listening()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    q: asyncio.Queue = asyncio.Queue()
    await global_listener.subscribe(q=q)
    try:
        while True:
            data = await q.get()
            await websocket.send_json(data)
    except WebSocketDisconnect:
        return


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
