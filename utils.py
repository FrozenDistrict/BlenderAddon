import bpy
import os
import random
import shutil

from .props import get_HF2_Mtz_list, get_HF2_Active_Mtz, get_HF2_Mtz_props, is_allowed_texture, category_fits_mtz_type
from .materializer_loader import assign_materializer
from .consts import TextureSuffixes, Defaults
from .data_exporter import export_data
from .export_exceptions import *
from mathutils import Vector
from .image_manipulation import set_alpha_to_0, combine_maos, invert_normal_map, save_as_rgba8_png

def set_mtz_category(category):
    mtz = get_HF2_Active_Mtz()
    mtz.materializer_category = category

def set_mtz_item_kind(item_kind):
    mtz = get_HF2_Active_Mtz()
    mtz.article_data.item_kind = item_kind
    
def set_mtz_item_series(item_series):
    mtz = get_HF2_Active_Mtz()
    mtz.article_data.item_series = item_series

def set_mtz_affordability(affordability):
    mtz = get_HF2_Active_Mtz()
    mtz.article_data.affordability = affordability

def set_mtz_shop_category(shop_category):
    mtz = get_HF2_Active_Mtz()
    mtz.article_data.shop_category = shop_category

def new_x_factor():
    used = {mtz.article_data.x_factor for mtz in get_HF2_Mtz_list()}
    unused = [x for x in range(Defaults.XFACTORMIN, Defaults.XFACTORMAX + 1) if x not in used]
    if not unused:
        return random.randint(Defaults.XFACTORMIN, Defaults.XFACTORMAX)
    return random.choice(unused)

def create_mtz():
    mtz = get_HF2_Mtz_list().add()
    mtz.article_data.x_factor = new_x_factor()
    return mtz

def remove_mtz():
    active_mtz_index = get_HF2_Mtz_props().active_mtz_index
    get_HF2_Mtz_list().remove(active_mtz_index)


def add_uv_unit_size():
    uv_unit_size = get_HF2_Active_Mtz().uv_unit_sizes.add()
    uv_unit_size.name = Defaults.UVUNITSIZE

    
def remove_un_unit_size():
    mtz = get_HF2_Active_Mtz()
    active_uv_unit_size_index = mtz.active_uv_unit_sizes_index
    mtz.uv_unit_sizes.remove(active_uv_unit_size_index)

def set_mtz_stid(mtz_stid):
    mtz = get_HF2_Active_Mtz()
    mtz.materializer_stid = mtz_stid

def add_mtz_stid(mtz_stid):
    mtz = get_HF2_Active_Mtz()
    existing_stids = [x.name for x in mtz.materializer_stids]
    if mtz_stid not in existing_stids:
        stid = mtz.materializer_stids.add()
        stid.name = mtz_stid

    
def remove_mtz_stid():
    mtz = get_HF2_Active_Mtz()
    active_mtz_stid_index = mtz.active_mtz_stid_index
    mtz.materializer_stids.remove(active_mtz_stid_index)


def create_icon_render_camera():
    props = get_HF2_Mtz_props()
    camera = props.icon_render_camera
    if not camera:
        bpy.ops.object.camera_add()
        camera = bpy.context.object
        props.icon_render_camera = camera
    
    camera.name = "MTZ Render Camera"

    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 1
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512
    bpy.context.scene.render.resolution_percentage = 100

    bpy.context.scene.camera = camera

    camera.location = (1.2, -1.700, 1.260)
    camera.rotation_euler = (1.04719755, 0, 0.6)


def unlink_object_from_all_collections(obj):
    for collection in bpy.data.collections:
        if obj.name in collection.objects:
            collection.objects.unlink(obj)
            
def unlink_from_main_scene(obj): 
    if(obj in bpy.context.scene.collection.objects.values()):
        bpy.context.scene.collection.objects.unlink(obj)

def create_preview_object(collection,material, name):
    bpy.ops.mesh.primitive_plane_add(size=3, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    plane = bpy.context.object
    unlink_object_from_all_collections(plane)
    plane.name = "%s Materializer Previewer" % (name)
    for poly in plane.data.polygons:
        poly.use_smooth = True
    plane.data.update()
    unlink_from_main_scene(plane)
    collection.objects.link(plane)
    return plane


def _create_world():
    if Defaults.WORLDNAME not in bpy.data.worlds:
        bpy.data.worlds.new(Defaults.WORLDNAME)

    world = bpy.data.worlds[Defaults.WORLDNAME]
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes.clear()
    background = world.node_tree.nodes.new('ShaderNodeBackground')
    background.inputs[0].default_value = (1, 1, 1, 1)
    
    output = world.node_tree.nodes.new("ShaderNodeOutputWorld")
    output.location = Vector((600.0, 0.0))

    world.node_tree.links.new(background.outputs[0], output.inputs[0])

def _create_sun(mtz):
    if(mtz.sun_preview):
        return
    bpy.ops.object.light_add(type='SUN', radius=1.0, location=(0,0,1), rotation=(1.1693706,-0.2443461,0))
    sun = bpy.context.object
    sun.data.energy = 5.0
    sun.data.color = (1.0,0.9,0.7)
    unlink_object_from_all_collections(sun)
    sun.name = "%s Materializer Previewer Sun" % (mtz.display_name)
    
    mtz.collection_preview.objects.link(sun)
    unlink_from_main_scene(sun)
    mtz.sun_preview = sun

def setup_lighting(mtz):
    _create_world()
    _create_sun(mtz)

def setup_height_displacement(mtz):
    obj = mtz.object_preview
    sub = obj.modifiers.new(name='Subdivision', type='SUBSURF')
    sub.subdivision_type = "SIMPLE"
    sub.levels = 7  
    sub.render_levels = 8  

    displace = mtz.object_preview.modifiers.new(name='Displace', type='DISPLACE')
    displace.strength = 0.2
    displace.texture_coords = 'UV'


    if not mtz.height_blend_texture:
        t = bpy.data.textures.new(mtz.display_name + " Displace Texture",'IMAGE')
        mtz.height_blend_texture = t

    mtz.height_blend_texture.image = mtz.height_texture
    displace.texture = mtz.height_blend_texture

def setup_composition():
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    
    for node in tree.nodes:
        tree.nodes.remove(node)
    
    render_layers_node = tree.nodes.new(type='CompositorNodeRLayers')
    render_layers_node.location = (-300, 300)
    
    filter_node = tree.nodes.new(type='CompositorNodeFilter')
    filter_node.filter_type = 'SHARPEN'
    filter_node.location = (0, 300)
    filter_node.inputs[0].default_value = 0.5
    
    composite_node = tree.nodes.new(type='CompositorNodeComposite')
    composite_node.location = (300, 300)
    
    links = tree.links
    links.new(render_layers_node.outputs['Image'], filter_node.inputs['Image'])
    links.new(filter_node.outputs['Image'], composite_node.inputs['Image'])
    
    viewer_node = tree.nodes.new(type='CompositorNodeViewer')
    viewer_node.location = (300, 0)
    links.new(filter_node.outputs['Image'], viewer_node.inputs['Image'])


def setup_preview_main():
    mtz = get_HF2_Active_Mtz()
    create_icon_render_camera()

    if(not mtz.collection_preview):
       collection = bpy.data.collections.new(mtz.display_name)
       mtz.collection_preview = collection
       bpy.context.scene.collection.children.link(collection)

    setup_lighting(mtz)
    
    if(not mtz.material_icon_preview):
        material = bpy.data.materials.new(mtz.display_name)
        setup_material(mtz, True, material)
    else:
        setup_material(mtz, True)
    
    if(mtz.object_preview != None):
        delete =[mtz.object_preview]
        mtz.object_preview = None
        with bpy.context.temp_override(selected_objects=delete):
            bpy.ops.object.delete()
        mtz.object_preview = create_preview_object(mtz.collection_preview, mtz.material_preview, mtz.display_name)
    else:
        mtz.object_preview = create_preview_object(mtz.collection_preview, mtz.material_preview, mtz.display_name)

    if len(mtz.object_preview.data.materials):
        mtz.object_preview.data.materials[0] = mtz.material_icon_preview
    else:
        mtz.object_preview.data.materials.append(mtz.material_icon_preview)

    if(mtz.height_texture):
        setup_height_displacement(mtz)

def setup_material(mtz, is_icon, material = None):
    if material != None:
        material.use_nodes = True
    
        if is_icon:
            material.name += " Icon"
            mtz.material_icon_preview = material

    if is_icon:
        assign_materializer(mtz.material_icon_preview, mtz, is_icon)
        

def _export_textures(mtz, mtz_path):
    if int(mtz.type) == 0:
        _export_textures_standard(mtz, mtz_path)
    if int(mtz.type) == 1:
        _export_textures_pattern(mtz, mtz_path)

def _export_textures_standard(mtz, mtz_path):
    if(mtz.main_texture):
        texture_path = mtz.main_texture.filepath_from_user()
        _copy_texture(texture_path,mtz_path, TextureSuffixes.BASECOLOR)

    if(mtz.normal_map_texture):
        texture_path = mtz.normal_map_texture.filepath_from_user()
        is_directx = mtz.normal_map_format == '1'
        dst = _copy_texture(texture_path,mtz_path, TextureSuffixes.NORMAL, force_png = is_directx)
        if(is_directx):
            invert_normal_map(dst)

    if(mtz.maos_texture_combined == '0'):
        if(mtz.maos_texture):
            texture_path = mtz.maos_texture.filepath_from_user()
            _copy_texture(texture_path,mtz_path, TextureSuffixes.MAOS)
    else:
        combine_maos(mtz, mtz_path)

    if(mtz.height_texture):
        texture_path = mtz.height_texture.filepath_from_user()
        _copy_texture(texture_path,mtz_path, TextureSuffixes.HEIGHT)
    
    if(mtz.mask_map_texture):
        texture_path = mtz.mask_map_texture.filepath_from_user()
        dst = _copy_texture(texture_path,mtz_path, TextureSuffixes.STANDARDCOLORMASK, force_png = mtz.invert_mask_alpha)
        if(mtz.invert_mask_alpha):
            set_alpha_to_0(dst)

    if(mtz.icon_texture):
        texture_path = mtz.icon_texture.filepath_from_user()
        _copy_texture(texture_path,mtz_path, TextureSuffixes.ICON)
    

def icon_can_be_rendered():
    mtz = get_HF2_Active_Mtz()
    return mtz.collection_preview and mtz.material_icon_preview and mtz.object_preview and mtz.sun_preview and get_HF2_Mtz_props().icon_render_camera

def _export_textures_pattern(mtz, mtz_path):
    if(mtz.color_map_texture):
        texture_path = mtz.color_map_texture.filepath_from_user()
        _copy_texture(texture_path,mtz_path, TextureSuffixes.COLORMAP)

    if(mtz.normal_map_texture):
        texture_path = mtz.normal_map_texture.filepath_from_user()
        _copy_texture(texture_path,mtz_path, TextureSuffixes.NORMAL)

    if(mtz.mask_map_texture):
        texture_path = mtz.mask_map_texture.filepath_from_user()
        dst = _copy_texture(texture_path,mtz_path, TextureSuffixes.MASKMAP, force_png = mtz.invert_mask_alpha)
        if(mtz.invert_mask_alpha):
            set_alpha_to_0(dst)

    if(mtz.icon_texture):
        texture_path = mtz.icon_texture.filepath_from_user()
        _copy_texture(texture_path,mtz_path, TextureSuffixes.ICON)
    

def _texture_path(source, target_directory, type, force_png = False):
    filename, file_extension = os.path.splitext(source)
    if force_png:
        file_extension = ".png"
    filename = "tex %s%s" % (type, file_extension)
    dst = os.path.join(target_directory, filename)
    return dst


def _copy_texture(source, target_directory, type, force_png = False):
    dst = _texture_path(source, target_directory, type, force_png)
    if(dst.lower().endswith(".png")):
        save_as_rgba8_png(source, dst)
    elif(source != dst):
        shutil.copyfile(source, dst)
    return dst


def _validate_uv_unit_sizes(uv_unit_sizes):
    if(not len(uv_unit_sizes)):
        add_uv_unit_size()
        return
    for x in uv_unit_sizes:
        try:
            float(x.name)
        except ValueError:
            raise UVScaleWrongFormat(x)
        
def _validate_mod_folder_path(mod_path):
    if(not os.path.isdir(mod_path)):
        raise HF2ModFolderInvalid(mod_path)

def _validate_mtz_number():
    if(not len(get_HF2_Mtz_list())):
        raise NoMTZ("Materializer") 
    
def _validate_stids(mtz):
    if not mtz.materializer_stid:
        raise EmptyData("Materializer Tag")
    if not mtz.materializer_category:
        raise EmptyData("Materializer category")
    if not category_fits_mtz_type(mtz.materializer_category, mtz.type):
        raise CategoryNotMatchingType(mtz.materializer_category.strip())

def is_power_of_two(n):
        return (n & (n - 1)) == 0 and n != 0 

def _get_exported_textures(mtz):
    if int(mtz.type) == 1:
        textures = [mtz.color_map_texture, mtz.normal_map_texture, mtz.mask_map_texture]
    else:
        textures = [mtz.main_texture, mtz.normal_map_texture, mtz.height_texture, mtz.mask_map_texture]
        if mtz.maos_texture_combined == '0':
            textures.append(mtz.maos_texture)
        else:
            textures += [mtz.metallic_texture, mtz.ao_texture, mtz.smoothness_texture]
    textures.append(mtz.icon_texture)
    return [tex for tex in textures if tex]

def _get_texture_size(tex):
    width, height = tex.size
    if width == 0 or height == 0:
        try:
            tex.reload()
        except RuntimeError:
            pass
        width, height = tex.size
    return width, height

def _validate_texture_formats(mtz):
    unsupported_textures = [tex.name for tex in _get_exported_textures(mtz) if not is_allowed_texture(tex)]
    if unsupported_textures:
        raise UnsupportedTextureFormat(", ".join(unsupported_textures))

def _has_png_textures(mtz):
    return any(tex.filepath.lower().endswith(".png") for tex in _get_exported_textures(mtz))

def _validate_textures_po2(mtz):
    unreadable_textures = []
    non_po2_textures = []
    for tex in _get_exported_textures(mtz):
        width, height = _get_texture_size(tex)
        if width == 0 or height == 0:
            unreadable_textures.append(tex.name)
        elif not is_power_of_two(width) or not is_power_of_two(height):
            non_po2_textures.append("%s (%dx%d)" % (tex.name, width, height))

    if unreadable_textures:
        raise TextureUnreadable(", ".join(unreadable_textures))
    if non_po2_textures:
        raise NoPO2(", ".join(non_po2_textures))


def _validate_pillow_pack(mtz):
    try:
        from PIL import Image
    except ImportError:
        raise PillowNotInstalled()

def _switch_to_collection(collection):
    view_layer = bpy.context.view_layer
    for layer_collection in view_layer.layer_collection.children:
        layer_collection.hide_viewport = layer_collection.name != collection.name

def _get_mod_folder_path(hf2_mc_path, mtz):
    
    mod_subfolder = Defaults.HF2MATERIALIZERFOLDERNAME
    if(mtz.type == '1'):
        mod_subfolder = Defaults.HF2PATTERNFOLDERNAME

    return os.path.join(hf2_mc_path,mod_subfolder,mtz.display_name)

def _validate_if_split_textures_are_same_size(mtz):
    sizes = []
    if mtz.metallic_texture:
        sizes.append(mtz.metallic_texture.size)
    if mtz.ao_texture:
        sizes.append(mtz.ao_texture.size)
    if mtz.smoothness_texture:
        sizes.append(mtz.smoothness_texture.size)

    if len(sizes) < 2:
        return
    first_size = sizes[0]
    for size in sizes:
        if size[0] != first_size[0] or size[1] != first_size[1]:
            raise SplitTexturesNotSameSize()



def render_icon_preview():
    mtz = get_HF2_Active_Mtz()
    mod_path = mtz.mod_path
    _validate_mod_folder_path(mod_path)
    _switch_to_collection(mtz.collection_preview)
    mod_path = _get_mod_folder_path(mod_path, mtz)

    icon_name = "tex %s.png" % TextureSuffixes.ICON
    icon_path = os.path.join(mod_path, icon_name)

    bpy.context.scene.render.filepath = icon_path
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.image_settings.color_depth = '8'
    bpy.context.scene.render.resolution_percentage = 100
    bpy.ops.render.render(write_still=True)

    icon = bpy.data.images.load(icon_path, check_existing=True)
    icon.reload()
    mtz.icon_texture = icon

    setup_composition()



def export_materializer():
    _validate_mtz_number()
    mtz = get_HF2_Active_Mtz()

    mod_path = mtz.mod_path 
    _validate_mod_folder_path(mod_path)
    _validate_uv_unit_sizes(mtz.uv_unit_sizes)
    _validate_stids(mtz)
    _validate_texture_formats(mtz)
    _validate_textures_po2(mtz)

    if(mtz.maos_texture_combined == '1'):
        _validate_if_split_textures_are_same_size(mtz)

    if(mtz.invert_mask_alpha or mtz.maos_texture_combined == '1' or mtz.normal_map_format == '1' or _has_png_textures(mtz)):
        _validate_pillow_pack(mtz)

    mod_path = _get_mod_folder_path(mod_path, mtz)

    if(not os.path.isdir(mod_path)):
        os.makedirs(mod_path)

    _export_textures(mtz, mod_path)
    export_data(mtz, mod_path)    
