#!/usr/bin/env python3
"""Blender MCP Server - FastMCP-based server for Blender integration."""

import json
import socket
import asyncio
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

try:
    from fastmcp import FastMCP
except ImportError:
    print("FastMCP not available. Install with: uv add fastmcp")
    exit(1)

class BlenderConnection:
    """Manages connection to Blender addon."""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self._socket = None
    
    async def connect(self) -> bool:
        """Connect to Blender addon."""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Failed to connect to Blender: {e}")
            return False
    
    async def send_command(self, command_type: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send command to Blender and get response."""
        if not self._socket:
            if not await self.connect():
                return {"status": "error", "message": "Not connected to Blender"}
        
        message = {
            "type": command_type,
            "params": params or {}
        }
        
        try:
            message_json = json.dumps(message)
            self._socket.send(message_json.encode('utf-8'))
            
            response_data = self._socket.recv(4096)
            response = json.loads(response_data.decode('utf-8'))
            return response
            
        except Exception as e:
            return {"status": "error", "message": f"Communication error: {e}"}
    
    def disconnect(self):
        """Disconnect from Blender."""
        if self._socket:
            self._socket.close()
            self._socket = None

# Global Blender connection
blender_conn = BlenderConnection()

# Initialize FastMCP server
mcp = FastMCP("Blender MCP Server")

# Object Management Tools
@mcp.tool
def create_object(
    object_type: str = Field(description="Type of object to create (CUBE, SPHERE, CYLINDER, PLANE)"),
    location: List[float] = Field(default=[0, 0, 0], description="XYZ location for the object"),
    name: Optional[str] = Field(default=None, description="Optional name for the object")
) -> Dict[str, Any]:
    """Create a new 3D object in Blender."""
    params = {
        "object_type": object_type.upper(),
        "location": location
    }
    if name:
        params["name"] = name
    
    return asyncio.run(blender_conn.send_command("create_object", params))

@mcp.tool
def delete_object(
    object_name: str = Field(description="Name of the object to delete")
) -> Dict[str, Any]:
    """Delete an object from the Blender scene."""
    params = {"object_name": object_name}
    return asyncio.run(blender_conn.send_command("delete_object", params))

@mcp.tool
def move_object(
    object_name: str = Field(description="Name of the object to move"),
    location: List[float] = Field(description="New XYZ location for the object")
) -> Dict[str, Any]:
    """Move an object to a new location."""
    params = {
        "object_name": object_name,
        "location": location
    }
    return asyncio.run(blender_conn.send_command("move_object", params))

@mcp.tool
def scale_object(
    object_name: str = Field(description="Name of the object to scale"),
    scale: List[float] = Field(description="XYZ scale factors")
) -> Dict[str, Any]:
    """Scale an object by the given factors."""
    params = {
        "object_name": object_name,
        "scale": scale
    }
    return asyncio.run(blender_conn.send_command("scale_object", params))

@mcp.tool
def rotate_object(
    object_name: str = Field(description="Name of the object to rotate"),
    rotation: List[float] = Field(description="XYZ rotation angles in radians")
) -> Dict[str, Any]:
    """Rotate an object by the given angles."""
    params = {
        "object_name": object_name,
        "rotation": rotation
    }
    return asyncio.run(blender_conn.send_command("rotate_object", params))

# Material Tools
@mcp.tool
def create_material(
    name: str = Field(description="Name for the new material"),
    color: List[float] = Field(default=[0.8, 0.8, 0.8, 1.0], description="RGBA color values (0-1)")
) -> Dict[str, Any]:
    """Create a new material with specified color."""
    params = {
        "name": name,
        "color": color
    }
    return asyncio.run(blender_conn.send_command("create_material", params))

@mcp.tool
def assign_material(
    object_name: str = Field(description="Name of the object"),
    material_name: str = Field(description="Name of the material to assign")
) -> Dict[str, Any]:
    """Assign a material to an object."""
    params = {
        "object_name": object_name,
        "material_name": material_name
    }
    return asyncio.run(blender_conn.send_command("assign_material", params))

@mcp.tool
def set_material_property(
    material_name: str = Field(description="Name of the material"),
    property_name: str = Field(description="Property to set (e.g., 'Base Color', 'Metallic', 'Roughness')"),
    value: Any = Field(description="Value to set for the property")
) -> Dict[str, Any]:
    """Set a property on a material."""
    params = {
        "material_name": material_name,
        "property_name": property_name,
        "value": value
    }
    return asyncio.run(blender_conn.send_command("set_material_property", params))

# Scene Management Tools
@mcp.tool
def get_scene_info() -> Dict[str, Any]:
    """Get information about the current Blender scene."""
    return asyncio.run(blender_conn.send_command("get_scene_info"))

@mcp.tool
def set_camera_position(
    location: List[float] = Field(description="XYZ location for the camera"),
    rotation: List[float] = Field(description="XYZ rotation angles for the camera")
) -> Dict[str, Any]:
    """Set the camera position and rotation."""
    params = {
        "location": location,
        "rotation": rotation
    }
    return asyncio.run(blender_conn.send_command("set_camera_position", params))

@mcp.tool
def render_scene(
    output_path: str = Field(description="Path to save the rendered image"),
    format: str = Field(default="PNG", description="Output format (PNG, JPEG, EXR, etc.)")
) -> Dict[str, Any]:
    """Render the current scene to an image file."""
    params = {
        "output_path": output_path,
        "format": format.upper()
    }
    return asyncio.run(blender_conn.send_command("render_scene", params))

# Resources
@mcp.resource("blender://scene/objects")
def scene_objects() -> str:
    """List all objects in the current scene."""
    result = asyncio.run(blender_conn.send_command("get_scene_info"))
    if result.get("status") == "success":
        objects = result.get("result", {}).get("objects", [])
        return json.dumps(objects, indent=2)
    return f"Error: {result.get('message', 'Unknown error')}"

@mcp.resource("blender://scene/materials")
def material_list() -> str:
    """List all available materials."""
    result = asyncio.run(blender_conn.send_command("get_materials"))
    if result.get("status") == "success":
        materials = result.get("result", [])
        return json.dumps(materials, indent=2)
    return f"Error: {result.get('message', 'Unknown error')}"

@mcp.resource("blender://object/{object_name}")
def object_properties(object_name: str) -> str:
    """Get detailed properties of a specific object."""
    result = asyncio.run(blender_conn.send_command("get_object_info", {"object_name": object_name}))
    if result.get("status") == "success":
        return json.dumps(result.get("result"), indent=2)
    return f"Error: {result.get('message', 'Unknown error')}"

# Prompts
@mcp.prompt("create_basic_scene")
def create_basic_scene() -> str:
    """Template for creating a basic 3D scene."""
    return """Create a basic 3D scene with the following steps:

1. Clear the default scene (delete default cube if present)
2. Create a plane as the ground
3. Add a cube above the plane
4. Add a sphere next to the cube
5. Create a basic material and apply it to objects
6. Position the camera for a good view
7. Add basic lighting

Example commands:
- delete_object("Cube")
- create_object("PLANE", [0, 0, 0], "Ground")
- create_object("CUBE", [0, 0, 1], "MainCube")
- create_object("SPHERE", [2, 0, 1], "MainSphere")
- create_material("BasicMaterial", [0.8, 0.2, 0.2, 1.0])
- assign_material("MainCube", "BasicMaterial")
"""

@mcp.prompt("lighting_setup")
def lighting_setup() -> str:
    """Standard lighting configurations for scenes."""
    return """Common lighting setups for 3D scenes:

**Three-Point Lighting:**
1. Key Light: Main light source, positioned at 45° to subject
2. Fill Light: Softer light to fill shadows, opposite side of key
3. Rim Light: Behind subject to separate from background

**HDRI Environment Lighting:**
- Use high dynamic range images for realistic lighting
- Provides ambient lighting and reflections
- Good for product visualization

**Studio Lighting:**
- Controlled environment with multiple light sources
- Soft boxes and area lights for even illumination
- Suitable for character and product rendering
"""

@mcp.prompt("material_workflow")
def material_workflow() -> str:
    """Material creation and assignment workflow."""
    return """Material Creation Workflow:

1. **Create Base Material:**
   - Use create_material() with descriptive name
   - Set base color and basic properties

2. **Configure Material Properties:**
   - Base Color: Main surface color
   - Metallic: 0.0 for non-metals, 1.0 for metals
   - Roughness: 0.0 for mirror, 1.0 for rough surfaces
   - Normal: For surface detail without geometry

3. **Assign to Objects:**
   - Use assign_material() to apply to objects
   - Multiple objects can share the same material

4. **Test and Refine:**
   - Render preview to see results
   - Adjust properties as needed
   - Consider lighting interaction

Example:
```
create_material("MetalMaterial", [0.8, 0.8, 0.9, 1.0])
set_material_property("MetalMaterial", "Metallic", 1.0)
set_material_property("MetalMaterial", "Roughness", 0.1)
assign_material("MyObject", "MetalMaterial")
```
"""

def main():
    """Main entry point for the MCP server."""
    print("Starting Blender MCP Server...")
    print("Make sure Blender is running with the MCP addon enabled.")
    
    try:
        # Run with HTTP transport for CLI client compatibility
        mcp.run(transport="ws", host="localhost", port=8000)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        blender_conn.disconnect()

if __name__ == "__main__":
    main()