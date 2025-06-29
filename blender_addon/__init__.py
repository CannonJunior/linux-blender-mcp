bl_info = {
    "name": "Blender MCP Addon",
    "author": "Custom Blender MCP",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > MCP",
    "description": "Model Context Protocol integration for Blender",
    "category": "System",
    "support": "COMMUNITY",
}

import bpy
from . import addon

def register():
    addon.register()

def unregister():
    addon.unregister()

if __name__ == "__main__":
    register()