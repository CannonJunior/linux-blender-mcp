"""Scene management and rendering tools for Blender MCP."""

from typing import Any, Dict, List, Optional, Tuple
from pydantic import Field

def setup_lighting(
    lighting_type: str = Field(default="THREE_POINT", description="Type of lighting setup"),
    key_light_position: List[float] = Field(default=[5, 5, 5], description="Position of key light"),
    key_light_energy: float = Field(default=1000, description="Energy of key light"),
    fill_light_energy: float = Field(default=500, description="Energy of fill light"),
    rim_light_energy: float = Field(default=750, description="Energy of rim light")
) -> Dict[str, Any]:
    """Set up scene lighting."""
    params = {
        "lighting_type": lighting_type,
        "key_light_position": key_light_position,
        "key_light_energy": key_light_energy,
        "fill_light_energy": fill_light_energy,
        "rim_light_energy": rim_light_energy
    }
    
    return {
        "command": "setup_lighting",
        "params": params
    }

def add_hdri_environment(
    hdri_path: str = Field(description="Path to HDRI image file"),
    rotation: float = Field(default=0.0, description="Rotation of the HDRI in radians"),
    strength: float = Field(default=1.0, description="Strength of the environment lighting")
) -> Dict[str, Any]:
    """Add HDRI environment lighting."""
    params = {
        "hdri_path": hdri_path,
        "rotation": rotation,
        "strength": strength
    }
    
    return {
        "command": "add_hdri_environment",
        "params": params
    }

def set_render_settings(
    engine: str = Field(default="CYCLES", description="Render engine (CYCLES, EEVEE, WORKBENCH)"),
    samples: int = Field(default=128, description="Number of render samples"),
    resolution_x: int = Field(default=1920, description="Render width"),
    resolution_y: int = Field(default=1080, description="Render height"),
    output_format: str = Field(default="PNG", description="Output file format")
) -> Dict[str, Any]:
    """Configure render settings."""
    params = {
        "engine": engine,
        "samples": samples,
        "resolution_x": resolution_x,
        "resolution_y": resolution_y,
        "output_format": output_format
    }
    
    return {
        "command": "set_render_settings",
        "params": params
    }

def create_camera_track(
    target_object: str = Field(description="Name of object for camera to track"),
    camera_positions: List[List[float]] = Field(description="List of camera positions for animation"),
    frame_duration: int = Field(default=24, description="Frames per position")
) -> Dict[str, Any]:
    """Create a camera animation track."""
    params = {
        "target_object": target_object,
        "camera_positions": camera_positions,
        "frame_duration": frame_duration
    }
    
    return {
        "command": "create_camera_track",
        "params": params
    }

def batch_render(
    output_directory: str = Field(description="Directory for output files"),
    frame_start: int = Field(default=1, description="Start frame"),
    frame_end: int = Field(default=250, description="End frame"),
    frame_step: int = Field(default=1, description="Frame step")
) -> Dict[str, Any]:
    """Render an animation sequence."""
    params = {
        "output_directory": output_directory,
        "frame_start": frame_start,
        "frame_end": frame_end,
        "frame_step": frame_step
    }
    
    return {
        "command": "batch_render",
        "params": params
    }

def import_model(
    file_path: str = Field(description="Path to model file"),
    file_format: str = Field(default="AUTO", description="File format (FBX, OBJ, GLTF, AUTO)"),
    scale: float = Field(default=1.0, description="Import scale factor"),
    location: List[float] = Field(default=[0, 0, 0], description="Import location")
) -> Dict[str, Any]:
    """Import a 3D model file."""
    params = {
        "file_path": file_path,
        "file_format": file_format,
        "scale": scale,
        "location": location
    }
    
    return {
        "command": "import_model",
        "params": params
    }

def export_scene(
    file_path: str = Field(description="Output file path"),
    file_format: str = Field(default="FBX", description="Export format (FBX, OBJ, GLTF, etc.)"),
    selected_only: bool = Field(default=False, description="Export only selected objects"),
    include_materials: bool = Field(default=True, description="Include materials in export"),
    include_textures: bool = Field(default=True, description="Include textures in export")
) -> Dict[str, Any]:
    """Export the scene or selected objects."""
    params = {
        "file_path": file_path,
        "file_format": file_format,
        "selected_only": selected_only,
        "include_materials": include_materials,
        "include_textures": include_textures
    }
    
    return {
        "command": "export_scene",
        "params": params
    }

def create_collection(
    name: str = Field(description="Name for the new collection"),
    parent_collection: Optional[str] = Field(default=None, description="Parent collection name")
) -> Dict[str, Any]:
    """Create a new collection for organizing objects."""
    params = {
        "name": name
    }
    if parent_collection:
        params["parent_collection"] = parent_collection
    
    return {
        "command": "create_collection",
        "params": params
    }

def move_to_collection(
    object_names: List[str] = Field(description="Names of objects to move"),
    collection_name: str = Field(description="Target collection name")
) -> Dict[str, Any]:
    """Move objects to a collection."""
    params = {
        "object_names": object_names,
        "collection_name": collection_name
    }
    
    return {
        "command": "move_to_collection",
        "params": params
    }

def set_viewport_shading(
    shading_type: str = Field(default="MATERIAL", description="Viewport shading mode"),
    show_overlays: bool = Field(default=True, description="Show overlays"),
    show_wireframe: bool = Field(default=False, description="Show wireframe")
) -> Dict[str, Any]:
    """Set viewport display settings."""
    params = {
        "shading_type": shading_type,
        "show_overlays": show_overlays,
        "show_wireframe": show_wireframe
    }
    
    return {
        "command": "set_viewport_shading",
        "params": params
    }