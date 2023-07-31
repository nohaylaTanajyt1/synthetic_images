import os
import json
import bpy
import bpy_extras
import random

json_file_path = '/baie/nfs-cluster-1/data1/raid1/homedirs/nohayla.tanajyt/Stage/ScenesAssets/farm/json_files/obj5.json'

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

def get_camera_coords(cam, pos):
    scene = bpy.context.scene
    x, y, z = bpy_extras.object_utils.world_to_camera_view(scene, cam, pos)
    scale = scene.render.resolution_percentage / 100.0
    w = int(scale * scene.render.resolution_x)
    h = int(scale * scene.render.resolution_y)
    px = int(round(x * w))
    py = int(round(h - y * h))
    return (px, py, z)

base_dir = '/baie/nfs-cluster-1/data1/raid1/homedirs/nohayla.tanajyt/Stage/ScenesAssets/farm/'

scn = bpy.context.scene
node_tree = scn.world.node_tree
tree_nodes = node_tree.nodes

scn.world.use_nodes = True

tree_nodes.clear()

node_background = tree_nodes.new(type='ShaderNodeBackground')
node_environment = tree_nodes.new('ShaderNodeTexEnvironment')
node_mapping = tree_nodes.new('ShaderNodeMapping')
node_output = tree_nodes.new(type='ShaderNodeOutputWorld')

def delete_textures(obj):
    for material_slot in obj.material_slots:
        material = material_slot.material
        if material:
            nodes = material.node_tree.nodes
            texture_nodes = [node for node in nodes if node.type == 'TEX_IMAGE']
            for node in texture_nodes:
                nodes.remove(node)

def add_texture(obj, image_path):
    if not os.path.exists(image_path):
        print(f"Warning: Texture file not found at '{image_path}'. Ignoring texture for object.")
        return
    
    if len(obj.data.materials) == 0:
        material = bpy.data.materials.new(name="Texture Material")
        obj.data.materials.append(material)
    else:
        material = obj.data.materials[0]

    texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    texture_node.image = bpy.data.images.load(image_path)
    material.node_tree.links.new(texture_node.outputs['Color'], material.node_tree.nodes['Principled BSDF'].inputs['Base Color'])


background_image_dir = os.path.join(base_dir, 'bkg')
img_name = 'clarens_night_02_4k.exr'
img_path = os.path.join(background_image_dir, img_name)
node_environment.image = bpy.data.images.load(img_path)

scale_value = 0.5
node_mapping.inputs[3].default_value = (scale_value, scale_value, scale_value)

links = node_tree.links
link = links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
link = links.new(node_background.outputs["Background"], node_output.inputs["Surface"])

with open(json_file_path, 'r') as json_file:
    proper = json.load(json_file)
    
objects = proper["objects"]

for obj_data in objects:
    object_name = obj_data["name"]
    file_path = obj_data["path"]
    location = obj_data["location"]
    rotation = obj_data["rotation"]
    scale = obj_data["scale"]
    textures = obj_data["texture"]
   
    obj_file_path = os.path.join(file_path)

    with bpy.data.libraries.load(obj_file_path) as (data_from, data_to):
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        bpy.context.scene.collection.objects.link(obj)

    for obj in bpy.data.objects:
        if obj.name == object_name:
            obj.location = location
            obj.rotation_euler = rotation
                    
            if isinstance(scale, list) and len(scale) == 3:
                obj.scale = scale  
            
            if obj.data:
                delete_textures(obj)

                if textures:
                    texture_path = random.choice(textures)
                    add_texture(obj, texture_path)
                else:
                    print(f"Object '{obj.name}' has no textures. Ignoring texture assignment.")
            else:
                print(f"Object '{obj.name}' has no valid geometry. Ignoring object.")



bpy.context.scene.render.engine = 'CYCLES'

bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'

bpy.context.preferences.addons['cycles'].preferences.devices[0].use = True

bpy.context.scene.cycles.samples = 4000

camera_name = "Camera" 
camera_obj = bpy.data.objects.get(camera_name)

if camera_obj is None:
    print(f"Camera object '{camera_name}' not found in the scene. Cannot render.")
else:
    bpy.context.scene.camera = camera_obj

output_dir = os.path.join(base_dir, 'outputs')
output_file = os.path.join(output_dir, f"farm_3_a.jpg")
bpy.context.scene.render.image_settings.file_format = "JPEG"
bpy.context.scene.render.filepath = output_file

bpy.context.scene.render.resolution_x = 550
bpy.context.scene.render.resolution_y = 413

bpy.ops.render.render(write_still=True)