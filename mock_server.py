#!/usr/bin/env python3
"""Mock Blender server for testing commands."""

import socket
import json
import threading

def mock_blender_server():
    """Run a mock server that responds like Blender addon."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8765))
    server.listen(1)
    print("🔧 Mock Blender server running on localhost:8765")
    
    try:
        while True:
            client, addr = server.accept()
            data = client.recv(4096)
            message = json.loads(data.decode('utf-8'))
            
            # Mock response
            if message.get("type") == "create_object":
                response = {
                    "status": "success",
                    "result": {
                        "name": message["params"].get("name", "MockObject"),
                        "location": message["params"].get("location", [0, 0, 0]),
                        "type": message["params"].get("object_type", "CUBE")
                    }
                }
            else:
                response = {
                    "status": "success",
                    "result": f"Mock response for {message.get('type')}"
                }
            
            client.send(json.dumps(response).encode('utf-8'))
            client.close()
            print(f"📝 Processed: {message.get('type')} - {message.get('params', {})}")
            
    except KeyboardInterrupt:
        print("\n🛑 Mock server stopped")
    finally:
        server.close()

if __name__ == "__main__":
    mock_blender_server()