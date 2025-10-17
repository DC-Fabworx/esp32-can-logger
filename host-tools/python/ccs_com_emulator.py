
import yaml, os, time, json, websockets, serial

CONF = yaml.safe_load(open(os.path.join('configs','ccs.yml'),'r',encoding='utf-8'))
SRC_WS = CONF['source']['websocket_url']
COM_OUT = CONF['serial']['com_out']
BAUD = int(CONF['serial']['baud'])

def to_line(d):
    # simple GVRET-like text line: id,datahex
    return f"{hex(d['id'])},{d['data']}\r\n".encode('ascii')

async def run():
    print(f"CCS Serial emulator -> {COM_OUT}@{BAUD} from {SRC_WS}")
    with serial.Serial(COM_OUT, BAUD, timeout=0.1) as ser:
        async for ws in websockets.connect(SRC_WS, ping_interval=20, ping_timeout=20):
            try:
                while True:
                    msg = await ws.recv()
                    d = json.loads(msg)
                    ser.write(to_line(d))
            except Exception as e:
                print("serial emu error:", e)

import asyncio
asyncio.run(run())
