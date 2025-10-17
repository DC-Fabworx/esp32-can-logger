
import serial, socket, time, yaml, os, sys

CONF_PATH = os.path.join('configs','serial.yml')
CONF = yaml.safe_load(open(CONF_PATH, 'r', encoding='utf-8')) if os.path.exists(CONF_PATH) else {}

COM = CONF.get('com_port', 'COM3')
BAUD = int(CONF.get('baud', 115200))
UDP_HOST = CONF.get('udp_host', '127.0.0.1')
UDP_PORT = int(CONF.get('udp_port', 19001))

def main():
    print(f"Serial->UDP {COM}@{BAUD} -> {UDP_HOST}:{UDP_PORT}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        with serial.Serial(COM, BAUD, timeout=0.1) as ser:
            while True:
                data = ser.read(1024)
                if data:
                    sock.sendto(data, (UDP_HOST, UDP_PORT))
                time.sleep(0.001)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
