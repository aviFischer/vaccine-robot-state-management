import sseclient

messages = sseclient.SSEClient('http://localhost:5000/state_stream')

for msg in messages:
    print(msg)
