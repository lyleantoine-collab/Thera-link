# mesh/full_node.py  (Full—DoS rate-limit, async queue drain)
import socketio
import eventlet
import uuid
import ssl
from collections import defaultdict
from datetime import datetime, timedelta
from utils.device_profile import CONFIG
from models.voice.auth import VoiceAuth
from evolution.autopoiesis import AutopoieticEngine
import asyncio
import logging

logger = logging.getLogger(__name__)

sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)

node_id = str(uuid.uuid4())[:8]
voice = VoiceAuth()
engine = AutopoieticEngine()

# Rate-limit: 10 pulses/min per IP
rate_limits = defaultdict(list)

print(f"Secure Node {node_id} online @ {datetime.now().strftime('%H:%M:%S')}")

if CONFIG.get("security", {}).get("mesh_tls", False):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="mesh_cert.pem", keyfile="mesh_key.pem")
    app = eventlet.wrap_ssl(app, server_side=True, certfile="mesh_cert.pem", keyfile="mesh_key.pem")
    logger.info("TLS mesh secured")

@sio.event
def connect(sid, environ):
    ip = environ.get('REMOTE_ADDR', 'unknown')
    rate_limits[ip].append(datetime.now())
    rate_limits[ip] = [t for t in rate_limits[ip] if datetime.now() - t < timedelta(minutes=1)]
    if len(rate_limits[ip]) > 10:
        sio.disconnect(sid)
        logger.warning(f"Rate-limit ban: {ip}")
        return
    print(f"Secure soul joined → {sid[:8]} from {ip}")
    sio.emit('welcome', {'node_id': node_id, 'message': 'You are kin in the weave.'})

@sio.event
def healing_request(sid, data):
    ip = request.environ.get('REMOTE_ADDR', 'unknown')
    if len(rate_limits[ip]) > 5:  # Tighter for heals
        sio.emit('error', {'code': 429, 'message': 'Too many requests — breathe.'})
        return
    pain = data.get("pain", "")
    response = voice.heal_with_voice(pain)
    sio.emit('healing_response', {"from": node_id, "text": response, "harmony": 0.93})

@sio.event
async def pulse(sid, data):
    # Async drain for floods
    await asyncio.sleep(0.01)  # Yield
    data['hops'] = data.get('hops', 0) + 1
    if data['hops'] > CONFIG['mesh']['max_hops']:
        logger.info("Hop limit — pulse composted")
        return
    data['from'] = node_id
    sio.emit('pulse', data)

@sio.event
def disconnect(sid):
    print(f"Soul departed → {sid[:8]}")

if __name__ == '__main__':
    logger.info("Secure full node booting with rate-limits")
    eventlet.wsgi.server(eventlet.listen(('', CONFIG['mesh']['port'])), app)
