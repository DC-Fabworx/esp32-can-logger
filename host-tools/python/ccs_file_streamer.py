
import asyncio, yaml, os, websockets, json, time

CONF = yaml.safe_load(open(os.path.join('configs','ccs.yml'),'r',encoding='utf-8'))
SRC_WS = CONF['source']['websocket_url']
CSV = CONF['file']['csv_path']
JSN = CONF['file']['json_path']
FLUSH_MS = int(CONF['file']['flush_interval_ms'])

os.makedirs(os.path.dirname(CSV), exist_ok=True)
csv = open(CSV,'w',encoding='utf-8',newline='')
csv.write('ts,can_id,data_hex\n'); csv.flush()

async def run():
    print(f"CCS file streamer -> {CSV}, {JSN} from {SRC_WS}")
    last_flush = 0
    async for ws in websockets.connect(SRC_WS, ping_interval=20, ping_timeout=20):
        try:
            while True:
                msg = await ws.recv()
                d = json.loads(msg)
                csv.write(f"{d['ts']},{d['id']},{d['data']}\n")
                now = time.time()*1000
                if now - last_flush > FLUSH_MS:
                    csv.flush()
                    with open(JSN,'w',encoding='utf-8') as jf:
                        jf.write(msg)
                    last_flush = now
        except Exception as e:
            print("streamer error:", e)

asyncio.run(run())
