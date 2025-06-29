import bpy
import bmesh
import json
import socket
import threading
import time
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import BoolProperty, StringProperty, IntProperty

class BlenderMCPProperties(PropertyGroup):
    is_server_running: BoolProperty(
        name="Server Running",
        default=False
    )
    
    server_host: StringProperty(
        name="Host",
        default="localhost"
    )
    
    server_port: IntProperty(
        name="Port",
        default=8765,
        min=1024,
        max=65535
    )

class BlenderMCPServer:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.thread = None
    
    def start(self):
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_server)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.thread:
            self.thread.join(timeout=1)
    
    def _run_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Blender MCP Server listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    self.server_socket.settimeout(1.0)
                    client_socket, addr = self.server_socket.accept()
                    print(f"Connection from {addr}")
                    
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"Server error: {e}")
                    break
                    
        except Exception as e:
            print(f"Failed to start server: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def _handle_client(self, client_socket):
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    message = json.loads(data.decode('utf-8'))
                    response = self._process_command(message)
                    
                    response_json = json.dumps(response)
                    client_socket.send(response_json.encode('utf-8'))
                    
                except json.JSONDecodeError:
                    error_response = {
                        "status": "error",
                        "message": "Invalid JSON"
                    }
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
                    
        except Exception as e:
            print(f"Client handler error: {e}")
        finally:
            client_socket.close()
    
    def _process_command(self, message):
        command_type = message.get("type")
        params = message.get("params", {})
        
        # Queue the command to run on the main thread
        result = {"status": "pending"}
        
        def execute_command():
            nonlocal result
            try:
                if command_type == "create_object":
                    result = self._create_object(params)
                elif command_type == "delete_object":
                    result = self._delete_object(params)
                elif command_type == "move_object":
                    result = self._move_object(params)
                elif command_type == "get_scene_info":
                    result = self._get_scene_info()
                elif command_type == "create_material":
                    result = self._create_material(params)
                elif command_type == "assign_material":
                    result = self._assign_material(params)
                else:
                    result = {
                        "status": "error",
                        "message": f"Unknown command: {command_type}"
                    }
            except Exception as e:
                result = {
                    "status": "error",
                    "message": str(e)
                }
            return None  # Don't repeat the timer
        
        # Execute immediately on main thread using timer
        bpy.app.timers.register(execute_command, first_interval=0.01)
        
        # Wait for execution (simple polling)
        import time
        timeout = 5.0
        start_time = time.time()
        while result["status"] == "pending" and (time.time() - start_time) < timeout:
            time.sleep(0.01)
        
        if result["status"] == "pending":
            return {
                "status": "error",
                "message": "Command execution timeout"
            }
        
        return result
    
    def _create_object(self, params):
        object_type = params.get("object_type", "CUBE")
        location = params.get("location", [0, 0, 0])
        name = params.get("name")
        
        try:
            if object_type == "CUBE":
                bpy.ops.mesh.primitive_cube_add(location=location)
            elif object_type == "SPHERE":
                bpy.ops.mesh.primitive_uv_sphere_add(location=location)
            elif object_type == "CYLINDER":
                bpy.ops.mesh.primitive_cylinder_add(location=location)
            elif object_type == "PLANE":
                bpy.ops.mesh.primitive_plane_add(location=location)
            else:
                return {
                    "status": "error",
                    "message": f"Unknown object type: {object_type}"
                }
            
            # Get the newly created object from the scene
            obj = None
            for o in bpy.data.objects:
                if o.select_get():
                    obj = o
                    break
            
            if not obj:
                # Fallback - get the last object in the scene
                if bpy.data.objects:
                    obj = bpy.data.objects[-1]
            
            if obj and name:
                obj.name = name
            
            return {
                "status": "success",
                "result": {
                    "name": obj.name if obj else "Unknown",
                    "location": list(obj.location) if obj else location,
                    "type": object_type
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create object: {str(e)}"
            }
    
    def _delete_object(self, params):
        object_name = params.get("object_name")
        
        if object_name not in bpy.data.objects:
            return {
                "status": "error",
                "message": f"Object '{object_name}' not found"
            }
        
        obj = bpy.data.objects[object_name]
        bpy.data.objects.remove(obj, do_unlink=True)
        
        return {
            "status": "success",
            "message": f"Object '{object_name}' deleted"
        }
    
    def _move_object(self, params):
        object_name = params.get("object_name")
        location = params.get("location", [0, 0, 0])
        
        if object_name not in bpy.data.objects:
            return {
                "status": "error",
                "message": f"Object '{object_name}' not found"
            }
        
        obj = bpy.data.objects[object_name]
        obj.location = location
        
        return {
            "status": "success",
            "result": {
                "name": object_name,
                "location": list(obj.location)
            }
        }
    
    def _get_scene_info(self):
        objects = []
        for obj in bpy.data.objects:
            objects.append({
                "name": obj.name,
                "type": obj.type,
                "location": list(obj.location),
                "rotation": list(obj.rotation_euler),
                "scale": list(obj.scale)
            })
        
        # Find active object safely
        active_object = None
        try:
            if hasattr(bpy.context, 'active_object') and bpy.context.active_object:
                active_object = bpy.context.active_object.name
        except:
            pass
        
        return {
            "status": "success",
            "result": {
                "objects": objects,
                "active_object": active_object
            }
        }
    
    def _create_material(self, params):
        name = params.get("name", "Material")
        color = params.get("color", [0.8, 0.8, 0.8, 1.0])
        
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
        
        return {
            "status": "success",
            "result": {
                "name": mat.name,
                "color": color
            }
        }
    
    def _assign_material(self, params):
        object_name = params.get("object_name")
        material_name = params.get("material_name")
        
        if object_name not in bpy.data.objects:
            return {
                "status": "error",
                "message": f"Object '{object_name}' not found"
            }
        
        if material_name not in bpy.data.materials:
            return {
                "status": "error", 
                "message": f"Material '{material_name}' not found"
            }
        
        obj = bpy.data.objects[object_name]
        mat = bpy.data.materials[material_name]
        
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        
        return {
            "status": "success",
            "message": f"Material '{material_name}' assigned to '{object_name}'"
        }

# Global server instance
mcp_server = None

class BLENDER_MCP_OT_start_server(Operator):
    bl_idname = "blender_mcp.start_server"
    bl_label = "Start MCP Server"
    
    def execute(self, context):
        global mcp_server
        props = context.scene.blender_mcp_props
        
        if mcp_server and mcp_server.running:
            self.report({'WARNING'}, "Server already running")
            return {'CANCELLED'}
        
        mcp_server = BlenderMCPServer(props.server_host, props.server_port)
        mcp_server.start()
        props.is_server_running = True
        
        self.report({'INFO'}, f"MCP Server started on {props.server_host}:{props.server_port}")
        return {'FINISHED'}

class BLENDER_MCP_OT_stop_server(Operator):
    bl_idname = "blender_mcp.stop_server"
    bl_label = "Stop MCP Server"
    
    def execute(self, context):
        global mcp_server
        props = context.scene.blender_mcp_props
        
        if mcp_server:
            mcp_server.stop()
            mcp_server = None
        
        props.is_server_running = False
        self.report({'INFO'}, "MCP Server stopped")
        return {'FINISHED'}

class BLENDER_MCP_PT_panel(Panel):
    bl_label = "Blender MCP"
    bl_idname = "BLENDER_MCP_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MCP"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.blender_mcp_props
        
        col = layout.column()
        col.prop(props, "server_host")
        col.prop(props, "server_port")
        
        if props.is_server_running:
            col.operator("blender_mcp.stop_server", text="Stop Server", icon='PAUSE')
            col.label(text="Status: Running", icon='CHECKMARK')
        else:
            col.operator("blender_mcp.start_server", text="Start Server", icon='PLAY')
            col.label(text="Status: Stopped", icon='X')

classes = [
    BlenderMCPProperties,
    BLENDER_MCP_OT_start_server,
    BLENDER_MCP_OT_stop_server,
    BLENDER_MCP_PT_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.blender_mcp_props = bpy.props.PointerProperty(
        type=BlenderMCPProperties
    )

def unregister():
    global mcp_server
    
    if mcp_server:
        mcp_server.stop()
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.blender_mcp_props