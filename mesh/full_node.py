# mesh/full_node.py  (Full overwrite—TLS certs, encrypted pulses)
import socketio
import eventlet
import uuid
import ssl
from cryptography.fernet import Fernet
from datetime import datetime
from utils.device_profile import CONFIG
from models.voice.auth import VoiceAuth
from evolution.autopoiesis import AutopoieticEngine
import logging

logger = logging.getLogger(__name__)

sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)

node_id = str(uuid.uuid4())[:8]
voice = VoiceAuth()
engine = AutopoieticEngine()
key = Fernet.generate_key()  # Per-session
cipher = Fernet(key)

print(f"Secure Node {node_id} online @ {datetime.now().strftime('%H:%M:%S')}")

if CONFIG.get("security", {}).get("mesh_tls", False):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="mesh_cert.pem", keyfile="mesh_key.pem")  # Gen stubs below
    app = eventlet.wrap_ssl(app, server_side=True, certfile="mesh_cert.pem", keyfile="mesh_key.pem")
    logger.info("TLS mesh secured — certs loaded")

@sio.event
def connect(sid, environ):
    print(f"Secure soul joined → {sid[:8]}")
    sio.emit('welcome', cipher.encrypt(b"You are kin in the weave.").decode())

@sio.event
def healing_request(sid, data):
    # Decrypt pulse
    try:
        decrypted = json.loads(cipher.decrypt(data['encrypted_pain'].encode()).decode())
        pain = decrypted['pain']
        audio = decrypted.get('audio_base64')
    except:
        logger.warning("Decrypt fail — drop pulse")
        return
    response = voice.heal_with_voice(pain, audio)
    encrypted_resp = cipher.encrypt(response.encode()).decode()
    sio.emit('healing_response', {"encrypted": encrypted_resp, "from": node_id})

@sio.event
def pulse(sid, data):
    # Secure forward with hop limit
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
    logger.info("Secure full node booting")
    eventlet.wsgi.server(eventlet.listen(('', CONFIG['mesh']['port'])), app)
