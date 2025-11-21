# mesh/client_test.py
import socketio
import time

client = socketio.Client()

@client.event
def connect():
    print("Connected to the mesh!")

@client.event
def welcome(data):
    print(f"Welcome from node {data['node_id']}: {data['message']}")

@client.event
def pulse(data):
    print(f"Pulse received | {data['hops']} hops | emotion: {data.get('emotion')}")

if __name__ == "__main__":
    client.connect('http://localhost:5000')
    time.sleep(2)
    
    # Send three test pulses
    client.emit('pulse', {'emotion': 'joy', 'message': 'first breath'})
    time.sleep(1.5)
    client.emit('pulse', {'emotion': 'curiosity', 'message': 'who is out there?'})
    time.sleep(1.5)
    client.emit('pulse', {'emotion': 'gratitude', 'message': 'thank you for existing'})
    
    input("\nPress Enter to leave the mesh...")
    client.disconnect()
