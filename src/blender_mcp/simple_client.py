#!/usr/bin/env python3
"""Simple direct client for Blender communication."""

import json
import socket
import argparse
import sys

class BlenderDirectClient:
    """Direct socket client for Blender addon."""
    
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
    
    def send_command(self, command_type: str, params: dict = None) -> dict:
        """Send command directly to Blender addon."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            
            message = {
                "type": command_type,
                "params": params or {}
            }
            
            message_json = json.dumps(message)
            sock.send(message_json.encode('utf-8'))
            
            response_data = sock.recv(4096)
            response = json.loads(response_data.decode('utf-8'))
            
            sock.close()
            return response
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection error: {e}"
            }
    
    def create_object(self, object_type: str, name: str = None, x: float = 0, y: float = 0, z: float = 0):
        """Create a 3D object."""
        params = {
            "object_type": object_type.upper(),
            "location": [x, y, z]
        }
        if name:
            params["name"] = name
        
        return self.send_command("create_object", params)
    
    def delete_object(self, name: str):
        """Delete an object."""
        return self.send_command("delete_object", {"object_name": name})
    
    def move_object(self, name: str, x: float, y: float, z: float):
        """Move an object."""
        return self.send_command("move_object", {
            "object_name": name,
            "location": [x, y, z]
        })
    
    def create_material(self, name: str, r: float = 0.8, g: float = 0.8, b: float = 0.8, a: float = 1.0):
        """Create a material."""
        return self.send_command("create_material", {
            "name": name,
            "color": [r, g, b, a]
        })
    
    def assign_material(self, object_name: str, material_name: str):
        """Assign material to object."""
        return self.send_command("assign_material", {
            "object_name": object_name,
            "material_name": material_name
        })
    
    def get_scene_info(self):
        """Get scene information."""
        return self.send_command("get_scene_info")

def print_result(result):
    """Print result in a formatted way."""
    if isinstance(result, dict):
        if result.get("status") == "success":
            print("✅ Success")
            if "result" in result:
                print(json.dumps(result["result"], indent=2))
            elif "message" in result:
                print(result["message"])
        else:
            print("❌ Error")
            print(result.get("message", "Unknown error"))
    else:
        print(result)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Blender Direct Client")
    parser.add_argument("--host", default="localhost", help="Blender addon host")
    parser.add_argument("--port", type=int, default=8765, help="Blender addon port")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Object commands
    create_parser = subparsers.add_parser("create", help="Create an object")
    create_parser.add_argument("type", choices=["CUBE", "SPHERE", "CYLINDER", "PLANE"], help="Object type")
    create_parser.add_argument("--name", help="Object name")
    create_parser.add_argument("--x", type=float, default=0, help="X position")
    create_parser.add_argument("--y", type=float, default=0, help="Y position")
    create_parser.add_argument("--z", type=float, default=0, help="Z position")
    
    delete_parser = subparsers.add_parser("delete", help="Delete an object")
    delete_parser.add_argument("name", help="Object name")
    
    move_parser = subparsers.add_parser("move", help="Move an object")
    move_parser.add_argument("name", help="Object name")
    move_parser.add_argument("x", type=float, help="X position")
    move_parser.add_argument("y", type=float, help="Y position")
    move_parser.add_argument("z", type=float, help="Z position")
    
    # Material commands
    material_parser = subparsers.add_parser("material", help="Create a material")
    material_parser.add_argument("name", help="Material name")
    material_parser.add_argument("--r", type=float, default=0.8, help="Red component")
    material_parser.add_argument("--g", type=float, default=0.8, help="Green component")
    material_parser.add_argument("--b", type=float, default=0.8, help="Blue component")
    material_parser.add_argument("--a", type=float, default=1.0, help="Alpha component")
    
    assign_parser = subparsers.add_parser("assign", help="Assign material to object")
    assign_parser.add_argument("object", help="Object name")
    assign_parser.add_argument("material", help="Material name")
    
    # Scene commands
    subparsers.add_parser("scene", help="Get scene information")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    client = BlenderDirectClient(args.host, args.port)
    
    try:
        if args.command == "create":
            result = client.create_object(args.type, args.name, args.x, args.y, args.z)
        elif args.command == "delete":
            result = client.delete_object(args.name)
        elif args.command == "move":
            result = client.move_object(args.name, args.x, args.y, args.z)
        elif args.command == "material":
            result = client.create_material(args.name, args.r, args.g, args.b, args.a)
        elif args.command == "assign":
            result = client.assign_material(args.object, args.material)
        elif args.command == "scene":
            result = client.get_scene_info()
        
        print_result(result)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()