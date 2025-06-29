#!/usr/bin/env python3
"""Blender MCP Client - Client for connecting to Blender MCP server."""

import json
import asyncio
import argparse
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

try:
    import aiohttp
except ImportError:
    print("aiohttp not available. Install with: uv add aiohttp")
    sys.exit(1)

class BlenderMCPClient:
    """Client for communicating with Blender MCP server."""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool via direct Blender connection (bypassing MCP server)."""
        # Connect directly to Blender addon for now
        import socket
        import json
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", 8765))
            
            message = {
                "type": tool_name.replace("_", "_"),  # Map tool names to command types
                "params": kwargs
            }
            
            # Map MCP tool names to Blender command types
            tool_mapping = {
                "create_object": "create_object",
                "delete_object": "delete_object", 
                "move_object": "move_object",
                "get_scene_info": "get_scene_info",
                "create_material": "create_material",
                "assign_material": "assign_material"
            }
            
            command_type = tool_mapping.get(tool_name, tool_name)
            message["type"] = command_type
            
            message_json = json.dumps(message)
            sock.send(message_json.encode('utf-8'))
            
            response_data = sock.recv(4096)
            response = json.loads(response_data.decode('utf-8'))
            
            sock.close()
            return response
            
        except Exception as e:
            return {
                "error": "Connection error",
                "message": str(e)
            }
    
    async def get_resource(self, resource_name: str) -> str:
        """Get a resource from the MCP server."""
        if not self.session:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        
        url = urljoin(self.server_url, f"/resources/{resource_name}")
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return f"Error: HTTP {response.status} - {await response.text()}"
        except Exception as e:
            return f"Connection error: {e}"
    
    async def get_prompt(self, prompt_name: str) -> str:
        """Get a prompt template from the MCP server."""
        if not self.session:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        
        url = urljoin(self.server_url, f"/prompts/{prompt_name}")
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return f"Error: HTTP {response.status} - {await response.text()}"
        except Exception as e:
            return f"Connection error: {e}"

class BlenderCLI:
    """Command-line interface for Blender MCP operations."""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
    
    async def create_object(self, object_type: str, x: float = 0, y: float = 0, z: float = 0, name: Optional[str] = None):
        """Create a new 3D object."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.call_tool(
                "create_object",
                object_type=object_type,
                location=[x, y, z],
                name=name
            )
            self._print_result(result)
    
    async def delete_object(self, name: str):
        """Delete an object."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.call_tool("delete_object", object_name=name)
            self._print_result(result)
    
    async def move_object(self, name: str, x: float, y: float, z: float):
        """Move an object."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.call_tool(
                "move_object",
                object_name=name,
                location=[x, y, z]
            )
            self._print_result(result)
    
    async def scale_object(self, name: str, x: float, y: float, z: float):
        """Scale an object."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.call_tool(
                "scale_object",
                object_name=name,
                scale=[x, y, z]
            )
            self._print_result(result)
    
    async def create_material(self, name: str, r: float = 0.8, g: float = 0.8, b: float = 0.8, a: float = 1.0):
        """Create a new material."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.call_tool(
                "create_material",
                name=name,
                color=[r, g, b, a]
            )
            self._print_result(result)
    
    async def assign_material(self, object_name: str, material_name: str):
        """Assign a material to an object."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.call_tool(
                "assign_material",
                object_name=object_name,
                material_name=material_name
            )
            self._print_result(result)
    
    async def scene_info(self):
        """Get scene information."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.call_tool("get_scene_info")
            self._print_result(result)
    
    async def list_objects(self):
        """List all objects in the scene."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.get_resource("scene/objects")
            print(result)
    
    async def render(self, output_path: str, format: str = "PNG"):
        """Render the scene."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.call_tool(
                "render_scene",
                output_path=output_path,
                format=format
            )
            self._print_result(result)
    
    async def get_prompt(self, prompt_name: str):
        """Get a prompt template."""
        async with BlenderMCPClient(self.server_url) as client:
            result = await client.get_prompt(prompt_name)
            print(result)
    
    def _print_result(self, result: Dict[str, Any]):
        """Print result in a formatted way."""
        if isinstance(result, dict):
            if "status" in result:
                if result["status"] == "success":
                    print("✅ Success")
                    if "result" in result:
                        print(json.dumps(result["result"], indent=2))
                    elif "message" in result:
                        print(result["message"])
                else:
                    print("❌ Error")
                    print(result.get("message", "Unknown error"))
            else:
                print(json.dumps(result, indent=2))
        else:
            print(result)

async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Blender MCP Client")
    parser.add_argument("--server", default="http://localhost:8000", help="MCP server URL")
    
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
    
    scale_parser = subparsers.add_parser("scale", help="Scale an object")
    scale_parser.add_argument("name", help="Object name")
    scale_parser.add_argument("x", type=float, help="X scale")
    scale_parser.add_argument("y", type=float, help="Y scale")
    scale_parser.add_argument("z", type=float, help="Z scale")
    
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
    subparsers.add_parser("objects", help="List all objects")
    
    # Render commands
    render_parser = subparsers.add_parser("render", help="Render the scene")
    render_parser.add_argument("output", help="Output file path")
    render_parser.add_argument("--format", default="PNG", help="Output format")
    
    # Prompt commands
    prompt_parser = subparsers.add_parser("prompt", help="Get a prompt template")
    prompt_parser.add_argument("name", choices=["create_basic_scene", "lighting_setup", "material_workflow"], help="Prompt name")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = BlenderCLI(args.server)
    
    try:
        if args.command == "create":
            await cli.create_object(args.type, args.x, args.y, args.z, args.name)
        elif args.command == "delete":
            await cli.delete_object(args.name)
        elif args.command == "move":
            await cli.move_object(args.name, args.x, args.y, args.z)
        elif args.command == "scale":
            await cli.scale_object(args.name, args.x, args.y, args.z)
        elif args.command == "material":
            await cli.create_material(args.name, args.r, args.g, args.b, args.a)
        elif args.command == "assign":
            await cli.assign_material(args.object, args.material)
        elif args.command == "scene":
            await cli.scene_info()
        elif args.command == "objects":
            await cli.list_objects()
        elif args.command == "render":
            await cli.render(args.output, args.format)
        elif args.command == "prompt":
            await cli.get_prompt(args.name)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Exception as e:
        print(f"Error: {e}")

def main_sync():
    """Synchronous entry point for the CLI."""
    asyncio.run(main())

if __name__ == "__main__":
    main_sync()