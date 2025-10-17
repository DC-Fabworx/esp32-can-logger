
import asyncio, yaml, os, websockets, json, urllib.request

CONF = yaml.safe_load(open(os.path.join('configs','ccs.yml'),'r',encoding='utf-8'))
SRC_WS = CONF['source']['websocket_url']
URL = CONF['rest']['url']
BATCH = int(CONF['rest']['batch_size'])

async def run():
    print(f"CCS REST push -> {URL} from {SRC_WS}")
    buf = []
    async for ws in websockets.connect(SRC_WS, ping_interval=20, ping_timeout=20):
        try:
            while True:
                msg = await ws.recv()
                buf.append(json.loads(msg))
                if len(buf) >= BATCH:
                    data = json.dumps(buf).encode('utf-8')
                    req = urllib.request.Request(URL, data=data, headers={'Content-Type':'application/json'})
                    try:
                        urllib.request.urlopen(req, timeout=2).read()
                    except Exception as e:
                        print("push error:", e)
                    buf.clear()
        except Exception as e:
            print("rest error:", e)

asyncio.run(run())
