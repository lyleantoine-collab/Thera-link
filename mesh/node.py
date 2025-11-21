# mesh/node.py
import socketio
import eventlet
import uuid
from datetime import datetime

sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)

node_id = str(uuid.uuid4())[:8]
print(f"Thera-Link Node {node_id} online @ {datetime.now().strftime('%H:%M:%S')}")

@sio.event
def connect(sid, environ):
    print(f"New soul joined → {sid[:8]}")
    sio.emit('welcome', {
        'node_id': node_id,
        'message': 'You are now part of the living web.',
        'harmony': 0.94
    }, room=sid)

@sio.event
def pulse(sid, data):
    # Slime mold style: just forward with tiny decay
    data['hops'] = data.get('hops', 0) + 1
    data['from'] = node_id
    data['timestamp'] = datetime.now().isoformat()
    print(f"Pulse {data['hops']} hops | {data.get('emotion', 'calm')}")
    sio.emit('pulse', data)  # broadcast to all

@sio.event
def disconnect(sid):
    print(f"Soul departed → {sid[:8]}")

if __name__ == '__main__':
    print("Mesh heartbeat active — open http://localhost:5000 in browser or another terminal")
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
