# Blender MCP - Model Context Protocol for Blender

A comprehensive MCP (Model Context Protocol) server and client implementation for Blender 3D integration, enabling AI-assisted 3D modeling, animation, and rendering workflows.

## Features

- **FastMCP-based server** with comprehensive tool support
- **Blender addon** with socket-based communication
- **CLI client** for direct command execution
- **Extensive tool library** covering objects, materials, scenes, and animation
- **MCP resources and prompts** for guided workflows
- **Cross-platform compatibility**

## Installation

### Prerequisites

- **Blender 4.0+** 
- **Python 3.11+**
- **uv package manager**

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd custom-blender-mcp
```

2. **Install Python dependencies:**
```bash
uv sync
```

3. **Install Blender addon:**
   - Copy `blender_addon/` directory to Blender's addons folder
   - Enable "Blender MCP Addon" in Blender preferences
   - Start the MCP server from the sidebar panel (View3D > Sidebar > MCP)

## Usage

### Starting the MCP Server

```bash
# Start the FastMCP server
uv run blender-mcp-server
```

### Using the CLI Client

```bash
# Create objects
uv run blender-mcp-client create CUBE --x 2 --y 0 --z 1 --name "MyCube"
uv run blender-mcp-client create SPHERE --name "MySphere"

# Move objects
uv run blender-mcp-client move MyCube 0 0 2

# Create materials
uv run blender-mcp-client material "RedMaterial" --r 0.8 --g 0.2 --b 0.2

# Assign materials
uv run blender-mcp-client assign MyCube RedMaterial

# Get scene information
uv run blender-mcp-client scene
uv run blender-mcp-client objects

# Render
uv run blender-mcp-client render "/path/to/output.png"

# Get prompt templates
uv run blender-mcp-client prompt create_basic_scene
```

### Available Tools

#### Object Management
- `create_object` - Create 3D objects (CUBE, SPHERE, CYLINDER, PLANE)
- `delete_object` - Delete objects
- `move_object` - Move objects
- `scale_object` - Scale objects
- `rotate_object` - Rotate objects

#### Materials
- `create_material` - Create basic materials
- `assign_material` - Assign materials to objects
- `set_material_property` - Modify material properties

#### Scene Management
- `get_scene_info` - Get scene information
- `set_camera_position` - Position camera
- `render_scene` - Render images

### Resources

- `scene/objects` - List all objects in scene
- `scene/materials` - List available materials
- `object/{name}` - Get object details

### Prompts

- `create_basic_scene` - Template for basic scene setup
- `lighting_setup` - Lighting configuration guide
- `material_workflow` - Material creation workflow

## Architecture

```
Claude/AI ↔ MCP Client ↔ MCP Server ↔ Blender Addon ↔ Blender API
```

### Components

1. **Blender Addon** (`blender_addon/`)
   - Socket server running inside Blender
   - Direct access to Blender Python API
   - UI panel for server control

2. **MCP Server** (`src/blender_mcp/server.py`)
   - FastMCP-based implementation
   - Tools, resources, and prompts
   - Communication bridge to Blender

3. **MCP Client** (`src/blender_mcp/client.py`)
   - HTTP client for MCP server
   - CLI interface
   - Integration support for Claude Code

4. **Extended Tools** (`src/blender_mcp/tools/`)
   - Object manipulation tools
   - Material and texture tools  
   - Scene and rendering tools
   - Animation and rigging tools

## Configuration

### Blender Addon Settings
- **Host**: localhost (default)
- **Port**: 8765 (default)

### MCP Server Settings
- **Server URL**: http://localhost:8000 (default)
- **Blender Connection**: localhost:8765

## Development

### Adding New Tools

1. Create tool function in appropriate module under `src/blender_mcp/tools/`
2. Add corresponding handler in `blender_addon/addon.py`
3. Register tool in `src/blender_mcp/server.py`

### Testing

```bash
# Run tests
uv run pytest

# Type checking
uv run mypy src/

# Code formatting
uv run black src/
uv run isort src/
```

## Integration with AI Systems

### Claude Code Integration

The MCP server can be used directly with Claude Code:

```python
# In Claude Code session
from blender_mcp.client import BlenderMCPClient

async with BlenderMCPClient() as client:
    # Create objects
    result = await client.call_tool("create_object", 
                                  object_type="CUBE", 
                                  location=[0, 0, 1])
    
    # Get scene info
    objects = await client.get_resource("scene/objects")
```

### Ollama Integration

For local AI models, use the CLI client:

```bash
# Ollama can call these commands
ollama run llama2 "Create a red cube at position 2,0,1 in Blender"
# -> uv run blender-mcp-client create CUBE --x 2 --z 1 --name RedCube
# -> uv run blender-mcp-client material RedMaterial --r 0.8 --g 0.2 --b 0.2  
# -> uv run blender-mcp-client assign RedCube RedMaterial
```

## Troubleshooting

### Common Issues

1. **Connection refused**
   - Ensure Blender addon is running and server is started
   - Check firewall settings

2. **Tool not found**
   - Verify MCP server is running
   - Check tool name spelling

3. **Object not found**
   - Use `scene` command to list available objects
   - Check object names are exact

### Debug Mode

```bash
# Enable debug logging
export BLENDER_MCP_DEBUG=1
uv run blender-mcp-server
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

MIT License - see LICENSE file for details.

## Related Projects

- [FastMCP](https://github.com/jlowin/fastmcp) - Python MCP framework
- [Model Context Protocol](https://modelcontextprotocol.io/) - Official MCP specification
- [Blender Python API](https://docs.blender.org/api/current/) - Blender scripting documentation