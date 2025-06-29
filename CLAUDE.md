# Blender MCP - Model Context Protocol Integration

## Product Vision

This repository implements a comprehensive MCP (Model Context Protocol) server and client for Blender 3D integration, enabling AI-assisted 3D modeling, animation, and rendering workflows.

## Architecture Components

### 1. Blender Addon (`blender_addon/`)
- Socket server running inside Blender (localhost:8765)
- Direct access to Blender Python API (`bpy` module)
- UI panel for server control and status
- Command handlers for all Blender operations

### 2. MCP Server (`src/blender_mcp/server.py`)
- FastMCP-based implementation following MCP specifications
- Comprehensive tools for objects, materials, scenes, animation
- Resources for scene inspection and data access
- Prompts for guided workflows and templates
- Communication bridge to Blender addon via TCP

### 3. MCP Client (`src/blender_mcp/client.py`)
- HTTP client for MCP server communication
- CLI interface for direct command execution
- Integration support for Claude Code and Ollama
- Async operations with proper error handling

### 4. Extended Tools (`src/blender_mcp/tools/`)
- **Object Tools**: Creation, manipulation, modifiers, parenting
- **Material Tools**: PBR materials, textures, procedural generation
- **Scene Tools**: Lighting, rendering, import/export, collections
- **Animation Tools**: Keyframes, armatures, constraints, shape keys

## Usage Patterns

### CLI Operations
```bash
# Object management
uv run blender-mcp-client create CUBE --x 2 --y 0 --z 1
uv run blender-mcp-client move MyCube 0 0 2

# Material workflow  
uv run blender-mcp-client material "RedMaterial" --r 0.8 --g 0.2 --b 0.2
uv run blender-mcp-client assign MyCube RedMaterial

# Scene operations
uv run blender-mcp-client scene
uv run blender-mcp-client render "/path/to/output.png"
```

### AI Integration
- **Claude Code**: Direct MCP client usage for interactive 3D modeling
- **Ollama**: CLI commands for local AI model integration
- **Agent2Agent**: Multi-agent workflows with delegation

## Development Guidelines

### Code Standards
- **Python 3.11+** with uv package management
- **FastMCP 2.0** for MCP server implementation
- **Pydantic** for data validation and type safety
- **AsyncIO** for non-blocking operations
- **Type hints** for all function signatures

### Tool Design Principles
1. **Simple but complete** - Each tool does one thing well
2. **Consistent parameters** - Standard naming across tools
3. **Comprehensive error handling** - Clear error messages
4. **Validation** - All inputs validated with Pydantic
5. **Documentation** - Tools, resources, and prompts well-documented

### Extending the System
1. **New Tools**: Add to appropriate module in `tools/`, implement handler in addon
2. **New Resources**: Add to server with proper caching
3. **New Prompts**: Create templates for common workflows
4. **New Features**: Follow MCP specification and FastMCP patterns

## Project Structure
```
blender-mcp/
├── pyproject.toml              # uv project configuration
├── src/blender_mcp/           # Main Python package
│   ├── server.py              # FastMCP server implementation
│   ├── client.py              # MCP client and CLI
│   └── tools/                 # Extended tool modules
├── blender_addon/             # Blender addon files
│   ├── __init__.py           # Addon registration
│   └── addon.py              # Main addon implementation
├── CLAUDE.md                  # This file - project context
└── README.md                  # User documentation
```

## Communication Flow
```
AI/User → MCP Client → MCP Server → Blender Addon → Blender API → 3D Scene
```

## Security & Validation
- All tool parameters validated with Pydantic schemas
- Socket communication with timeout and error handling
- File path validation for import/export operations
- No arbitrary code execution - only predefined tools

## Implementation Status
✅ Project structure with uv package management
✅ Blender addon with socket server and UI panel
✅ FastMCP server with core tools (objects, materials, scenes)
✅ MCP client with CLI interface
✅ Extended tools for advanced operations
✅ Resources and prompts for guided workflows
✅ Comprehensive documentation

# Rules
* 1. Use Python as a default. If there is a reason to develop a tool entirely or in part in another language, then stop to think step-by-step about the long-term utility of the tool. It may be that other tools previously developed should be refactored in this or other languages.
* 2. For Python, always use the uv package management project, documented here:
https://docs.astral.sh/uv/guides/install-python/
* 3. For tools, write them as Model Context Protocol compatible, documented here:
https://docs.anthropic.com/en/docs/mcp
Do not create a tool without also creating an MCP Server for the tool.
* 4. For agent interactions, write them consistent with the Agent2Agent protocol documented here:
https://github.com/a2aproject/a2a-python
* 5. When creating or working with agents, by default create a top level agent. This agent's only task is to delegate tasks to other agents while also checking credentials and providing them access to tools. If you plan on giving this top level agent tasks other than delegation, wait. Then stop and think step-by-step whether there is a better method than over-tasking the top level agent.
* 6. Whenever you create a new directory, create a CLAUDE.md file in that new directory. The purpose of CLAUDE.md includes
- Defining System Prompts: Users can write instructions or guidelines for the Claude Code agent within the CLAUDE.md file. This allows users to customize the AI's responses.
- Providing Context: Developers can use CLAUDE.md to define project conditions, best practices, or point the AI at codebases relevant to their workflow.
- Personal and Team Configurations: This file allows for both personal and team-level configurations, ensuring project standards.
- Enhancing AI Productivity: By providing context, CLAUDE.md helps improve the accuracy and relevance of the AI's responses, boosting developer productivity.
* 7. When creating agents and MCP tools, always make them as simple as possible, but no simpler.
* 8. With MCP tools, run them locally using the Python FastMCP library as a default. Ask the user for permission to consider other options.
