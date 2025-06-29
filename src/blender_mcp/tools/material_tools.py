"""Extended material manipulation tools for Blender MCP."""

from typing import Any, Dict, List, Optional
from pydantic import Field

def create_pbr_material(
    name: str = Field(description="Name for the PBR material"),
    base_color: List[float] = Field(default=[0.8, 0.8, 0.8, 1.0], description="Base color RGBA"),
    metallic: float = Field(default=0.0, description="Metallic value (0-1)"),
    roughness: float = Field(default=0.5, description="Roughness value (0-1)"),
    normal_strength: float = Field(default=1.0, description="Normal map strength"),
    emission_color: List[float] = Field(default=[0, 0, 0, 1], description="Emission color"),
    emission_strength: float = Field(default=0.0, description="Emission strength")
) -> Dict[str, Any]:
    """Create a PBR (Physically Based Rendering) material."""
    params = {
        "name": name,
        "base_color": base_color,
        "metallic": metallic,
        "roughness": roughness,
        "normal_strength": normal_strength,
        "emission_color": emission_color,
        "emission_strength": emission_strength
    }
    
    return {
        "command": "create_pbr_material",
        "params": params
    }

def add_texture_node(
    material_name: str = Field(description="Name of the material"),
    texture_path: str = Field(description="Path to the texture file"),
    node_type: str = Field(default="TEX_IMAGE", description="Type of texture node"),
    connection: str = Field(default="BASE_COLOR", description="Where to connect the texture")
) -> Dict[str, Any]:
    """Add a texture node to a material."""
    params = {
        "material_name": material_name,
        "texture_path": texture_path,
        "node_type": node_type,
        "connection": connection
    }
    
    return {
        "command": "add_texture_node",
        "params": params
    }

def create_material_from_images(
    name: str = Field(description="Name for the material"),
    diffuse_path: Optional[str] = Field(default=None, description="Path to diffuse/albedo texture"),
    normal_path: Optional[str] = Field(default=None, description="Path to normal map"),
    roughness_path: Optional[str] = Field(default=None, description="Path to roughness map"),
    metallic_path: Optional[str] = Field(default=None, description="Path to metallic map"),
    height_path: Optional[str] = Field(default=None, description="Path to height/displacement map")
) -> Dict[str, Any]:
    """Create a complete material from texture images."""
    params = {
        "name": name,
        "diffuse_path": diffuse_path,
        "normal_path": normal_path,
        "roughness_path": roughness_path,
        "metallic_path": metallic_path,
        "height_path": height_path
    }
    
    return {
        "command": "create_material_from_images",
        "params": params
    }

def duplicate_material(
    source_name: str = Field(description="Name of the source material"),
    new_name: str = Field(description="Name for the new material")
) -> Dict[str, Any]:
    """Duplicate an existing material."""
    params = {
        "source_name": source_name,
        "new_name": new_name
    }
    
    return {
        "command": "duplicate_material",
        "params": params
    }

def mix_materials(
    material1_name: str = Field(description="Name of the first material"),
    material2_name: str = Field(description="Name of the second material"),
    new_name: str = Field(description="Name for the mixed material"),
    mix_factor: float = Field(default=0.5, description="Mix factor (0-1)")
) -> Dict[str, Any]:
    """Mix two materials together."""
    params = {
        "material1_name": material1_name,
        "material2_name": material2_name,
        "new_name": new_name,
        "mix_factor": mix_factor
    }
    
    return {
        "command": "mix_materials",
        "params": params
    }

def create_procedural_material(
    name: str = Field(description="Name for the material"),
    material_type: str = Field(description="Type of procedural material (WOOD, MARBLE, NOISE, etc.)"),
    scale: float = Field(default=1.0, description="Scale of the procedural texture"),
    colors: List[List[float]] = Field(default=[[0.8, 0.8, 0.8, 1.0]], description="Colors for the material")
) -> Dict[str, Any]:
    """Create a procedural material."""
    params = {
        "name": name,
        "material_type": material_type,
        "scale": scale,
        "colors": colors
    }
    
    return {
        "command": "create_procedural_material",
        "params": params
    }

def setup_material_slots(
    object_name: str = Field(description="Name of the object"),
    material_names: List[str] = Field(description="List of material names to assign to slots")
) -> Dict[str, Any]:
    """Set up multiple material slots on an object."""
    params = {
        "object_name": object_name,
        "material_names": material_names
    }
    
    return {
        "command": "setup_material_slots",
        "params": params
    }

def bake_material(
    object_name: str = Field(description="Name of the object with material to bake"),
    bake_type: str = Field(default="COMBINED", description="Type of bake (COMBINED, DIFFUSE, NORMAL, etc.)"),
    output_path: str = Field(description="Path for the baked texture"),
    resolution: int = Field(default=1024, description="Resolution of the baked texture")
) -> Dict[str, Any]:
    """Bake a material to texture."""
    params = {
        "object_name": object_name,
        "bake_type": bake_type,
        "output_path": output_path,
        "resolution": resolution
    }
    
    return {
        "command": "bake_material",
        "params": params
    }