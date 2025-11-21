# mesh/discovery.py
import socket
import threading
import json
from datetime import datetime

DISCOVERY_PORT = 5005
BROADCAST_MSG = {"type": "thera_beacon", "node_id": "placeholder", "time": ""}

def start_broadcast(node_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BCCAST, 1)
    msg = json.dumps({**BROADCAST_MSG, "node_id": node_id, "time": datetime.now().isoformat()}).encode()
    def broadcast():
        while True:
            sock.sendto(msg, ('255.255.255.255', DISCOVERY_PORT))
            threading.Event().wait(3)
    threading.Thread(target=broadcast, daemon=True).start()
    print("Beacon active — other nodes will find me")

def listen_for_nodes(callback):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', DISCOVERY_PORT))
    def listener():
        while True:
            data, addr = sock.recvfrom(1024)
            msg = json.loads(data.decode())
            if msg["type"] == "thera_beacon" and msg["node_id"] != socket.gethostname():
                callback(msg, addr[0])
    threading.Thread(target=listener, daemon=True).start()
