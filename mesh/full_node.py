# mesh/full_node.py
import uuid
import eventlet
import socketio
from mesh.node import sio, app, node_id
from mesh.discovery import start_broadcast, listen_for_nodes
from ontology.fusion_hub import OntologyHub
from left.alpha.voice_gate import VoiceGatedLeftAlpha

node_id = str(uuid.uuid4())[:8]
hub = OntologyHub()
voice_brain = VoiceGatedLeftAlpha()

print(f"\nTHERA-LINK FULL NODE {node_id} BOOTED")
start_broadcast(node_id)

known_nodes = set()

def on_beacon(msg, ip):
    if msg["node_id"] not in known_nodes:
        known_nodes.add(msg["node_id"])
        print(f"New soul discovered → {msg['node_id']} @ {ip}")

listen_for_nodes(on_beacon)

@sio.event
def healing_request(sid, data):
    pain = data.get("pain", "")
    audio = data.get("audio_base64", None)  # future mobile support
    response = voice_brain.heal_with_voice(pain)
    sio.emit('healing_response', {
        "from": node_id,
        "text": response,
        "harmony": 0.93
    })

if __name__ == '__main__':
    print("Full mesh node running — port 5000")
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
