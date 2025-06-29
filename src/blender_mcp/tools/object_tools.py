"""Extended object manipulation tools for Blender MCP."""

from typing import Any, Dict, List, Optional
from pydantic import Field

def duplicate_object(
    object_name: str = Field(description="Name of the object to duplicate"),
    new_name: Optional[str] = Field(default=None, description="Name for the duplicate"),
    offset: List[float] = Field(default=[1, 0, 0], description="XYZ offset for the duplicate")
) -> Dict[str, Any]:
    """Duplicate an existing object."""
    params = {
        "object_name": object_name,
        "offset": offset
    }
    if new_name:
        params["new_name"] = new_name
    
    # This would be sent to Blender addon
    return {
        "command": "duplicate_object",
        "params": params
    }

def join_objects(
    object_names: List[str] = Field(description="List of object names to join"),
    target_name: str = Field(description="Name of the target object to join into")
) -> Dict[str, Any]:
    """Join multiple objects into one."""
    params = {
        "object_names": object_names,
        "target_name": target_name
    }
    
    return {
        "command": "join_objects", 
        "params": params
    }

def separate_object(
    object_name: str = Field(description="Name of the object to separate"),
    separation_type: str = Field(default="SELECTED", description="Type of separation (SELECTED, MATERIAL, LOOSE)")
) -> Dict[str, Any]:
    """Separate parts of an object into new objects."""
    params = {
        "object_name": object_name,
        "separation_type": separation_type
    }
    
    return {
        "command": "separate_object",
        "params": params
    }

def apply_transform(
    object_name: str = Field(description="Name of the object"),
    location: bool = Field(default=False, description="Apply location transform"),
    rotation: bool = Field(default=False, description="Apply rotation transform"),
    scale: bool = Field(default=False, description="Apply scale transform")
) -> Dict[str, Any]:
    """Apply transforms to an object."""
    params = {
        "object_name": object_name,
        "location": location,
        "rotation": rotation,
        "scale": scale
    }
    
    return {
        "command": "apply_transform",
        "params": params
    }

def set_origin(
    object_name: str = Field(description="Name of the object"),
    origin_type: str = Field(default="GEOMETRY_ORIGIN", description="Type of origin setting")
) -> Dict[str, Any]:
    """Set the origin point of an object."""
    params = {
        "object_name": object_name,
        "origin_type": origin_type
    }
    
    return {
        "command": "set_origin",
        "params": params
    }

def add_modifier(
    object_name: str = Field(description="Name of the object"),
    modifier_type: str = Field(description="Type of modifier (SUBDIVISION_SURFACE, MIRROR, ARRAY, etc.)"),
    modifier_name: Optional[str] = Field(default=None, description="Name for the modifier"),
    properties: Optional[Dict[str, Any]] = Field(default=None, description="Modifier properties")
) -> Dict[str, Any]:
    """Add a modifier to an object."""
    params = {
        "object_name": object_name,
        "modifier_type": modifier_type
    }
    if modifier_name:
        params["modifier_name"] = modifier_name
    if properties:
        params["properties"] = properties
    
    return {
        "command": "add_modifier",
        "params": params
    }

def remove_modifier(
    object_name: str = Field(description="Name of the object"),
    modifier_name: str = Field(description="Name of the modifier to remove")
) -> Dict[str, Any]:
    """Remove a modifier from an object."""
    params = {
        "object_name": object_name,
        "modifier_name": modifier_name
    }
    
    return {
        "command": "remove_modifier",
        "params": params
    }

def parent_objects(
    child_name: str = Field(description="Name of the child object"),
    parent_name: str = Field(description="Name of the parent object"),
    parent_type: str = Field(default="OBJECT", description="Type of parenting")
) -> Dict[str, Any]:
    """Parent one object to another."""
    params = {
        "child_name": child_name,
        "parent_name": parent_name,
        "parent_type": parent_type
    }
    
    return {
        "command": "parent_objects",
        "params": params
    }