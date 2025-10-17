
import asyncio, json, yaml, os, websockets, socket

CONF = yaml.safe_load(open(os.path.join('configs','ccs.yml'),'r',encoding='utf-8'))
SRC_WS = CONF['source']['websocket_url']
HOST, PORT = CONF['tcp']['host'], int(CONF['tcp']['port'])

async def pump(reader, writer):
    pass  # not used; we are client to CCS

async def forward():
    print(f"CCS TCP bridge -> {HOST}:{PORT} from {SRC_WS}")
    # connect UDP->WS source
    async for ws in websockets.connect(SRC_WS, ping_interval=20, ping_timeout=20):
        try:
            with socket.create_connection((HOST, PORT)) as s:
                while True:
                    msg = await ws.recv()
                    # msg expected: {'ts': float, 'id': int, 'data': 'hex'}
                    s.sendall((msg + "\n").encode('utf-8'))
        except Exception as e:
            print("bridge error:", e)

asyncio.run(forward())
