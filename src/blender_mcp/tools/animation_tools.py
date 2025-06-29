"""Animation and rigging tools for Blender MCP."""

from typing import Any, Dict, List, Optional, Tuple
from pydantic import Field

def add_keyframe(
    object_name: str = Field(description="Name of the object to animate"),
    property_name: str = Field(description="Property to keyframe (location, rotation, scale)"),
    frame: int = Field(description="Frame number for the keyframe"),
    value: List[float] = Field(description="Value for the keyframe")
) -> Dict[str, Any]:
    """Add a keyframe for object animation."""
    params = {
        "object_name": object_name,
        "property_name": property_name,
        "frame": frame,
        "value": value
    }
    
    return {
        "command": "add_keyframe",
        "params": params
    }

def create_animation_curve(
    object_name: str = Field(description="Name of the object"),
    property_name: str = Field(description="Property to animate"),
    keyframes: List[Tuple[int, List[float]]] = Field(description="List of (frame, value) pairs"),
    interpolation: str = Field(default="BEZIER", description="Interpolation type")
) -> Dict[str, Any]:
    """Create an animation curve with multiple keyframes."""
    params = {
        "object_name": object_name,
        "property_name": property_name,
        "keyframes": keyframes,
        "interpolation": interpolation
    }
    
    return {
        "command": "create_animation_curve",
        "params": params
    }

def add_armature(
    name: str = Field(default="Armature", description="Name for the armature"),
    location: List[float] = Field(default=[0, 0, 0], description="Location for the armature")
) -> Dict[str, Any]:
    """Add an armature for rigging."""
    params = {
        "name": name,
        "location": location
    }
    
    return {
        "command": "add_armature",
        "params": params
    }

def add_bone(
    armature_name: str = Field(description="Name of the armature"),
    bone_name: str = Field(description="Name for the new bone"),
    head_position: List[float] = Field(description="Head position of the bone"),
    tail_position: List[float] = Field(description="Tail position of the bone"),
    parent_bone: Optional[str] = Field(default=None, description="Parent bone name")
) -> Dict[str, Any]:
    """Add a bone to an armature."""
    params = {
        "armature_name": armature_name,
        "bone_name": bone_name,
        "head_position": head_position,
        "tail_position": tail_position
    }
    if parent_bone:
        params["parent_bone"] = parent_bone
    
    return {
        "command": "add_bone",
        "params": params
    }

def setup_ik_constraint(
    bone_name: str = Field(description="Name of the bone to constrain"),
    target_object: str = Field(description="Target object for IK"),
    chain_length: int = Field(default=2, description="Length of the IK chain")
) -> Dict[str, Any]:
    """Set up an IK (Inverse Kinematics) constraint."""
    params = {
        "bone_name": bone_name,
        "target_object": target_object,
        "chain_length": chain_length
    }
    
    return {
        "command": "setup_ik_constraint",
        "params": params
    }

def bind_mesh_to_armature(
    mesh_name: str = Field(description="Name of the mesh object"),
    armature_name: str = Field(description="Name of the armature"),
    binding_type: str = Field(default="AUTOMATIC", description="Type of binding")
) -> Dict[str, Any]:
    """Bind a mesh to an armature for deformation."""
    params = {
        "mesh_name": mesh_name,
        "armature_name": armature_name,
        "binding_type": binding_type
    }
    
    return {
        "command": "bind_mesh_to_armature",
        "params": params
    }

def create_shape_key(
    object_name: str = Field(description="Name of the mesh object"),
    shape_key_name: str = Field(description="Name for the shape key"),
    relative: bool = Field(default=True, description="Whether the shape key is relative")
) -> Dict[str, Any]:
    """Create a shape key for morphing animation."""
    params = {
        "object_name": object_name,
        "shape_key_name": shape_key_name,
        "relative": relative
    }
    
    return {
        "command": "create_shape_key",
        "params": params
    }

def animate_shape_key(
    object_name: str = Field(description="Name of the object"),
    shape_key_name: str = Field(description="Name of the shape key"),
    keyframes: List[Tuple[int, float]] = Field(description="List of (frame, value) pairs for animation")
) -> Dict[str, Any]:
    """Animate a shape key value."""
    params = {
        "object_name": object_name,
        "shape_key_name": shape_key_name,
        "keyframes": keyframes
    }
    
    return {
        "command": "animate_shape_key",
        "params": params
    }

def add_follow_path_constraint(
    object_name: str = Field(description="Name of the object to constrain"),
    path_object: str = Field(description="Name of the path object (curve)"),
    follow_axis: str = Field(default="FORWARD_Y", description="Axis to follow the path")
) -> Dict[str, Any]:
    """Add a follow path constraint for object animation."""
    params = {
        "object_name": object_name,
        "path_object": path_object,
        "follow_axis": follow_axis
    }
    
    return {
        "command": "add_follow_path_constraint",
        "params": params
    }

def set_animation_range(
    start_frame: int = Field(description="Start frame of the animation"),
    end_frame: int = Field(description="End frame of the animation")
) -> Dict[str, Any]:
    """Set the animation frame range."""
    params = {
        "start_frame": start_frame,
        "end_frame": end_frame
    }
    
    return {
        "command": "set_animation_range",
        "params": params
    }

def play_animation(
    play: bool = Field(default=True, description="Whether to play or pause animation")
) -> Dict[str, Any]:
    """Control animation playback."""
    params = {
        "play": play
    }
    
    return {
        "command": "play_animation",
        "params": params
    }

def bake_animation(
    object_name: str = Field(description="Name of the object"),
    start_frame: int = Field(description="Start frame for baking"),
    end_frame: int = Field(description="End frame for baking"),
    step: int = Field(default=1, description="Frame step for baking")
) -> Dict[str, Any]:
    """Bake animation data to keyframes."""
    params = {
        "object_name": object_name,
        "start_frame": start_frame,
        "end_frame": end_frame,
        "step": step
    }
    
    return {
        "command": "bake_animation",
        "params": params
    }