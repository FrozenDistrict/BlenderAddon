import os
import bpy
from enum import Enum
from mathutils import Vector
from .consts import Defaults

def setup_albedo(t_node, master_node, n_tree, mask_map = None):
    t_node.location = Vector((-600.0, 800.0))
    if mask_map == None: 
        n_tree.links.new(t_node.outputs[0], master_node.inputs[0])
    else:
        mix = n_tree.nodes.new("ShaderNodeMixRGB")
        mix.location = Vector((0,800.0))
        mix.blend_type = 'MULTIPLY'
        mix.inputs[0].default_value = 1

        n_tree.links.new(t_node.outputs[0],mix.inputs[1])
        n_tree.links.new(mask_map.outputs[0],mix.inputs[2])
        n_tree.links.new(mix.outputs[0],master_node.inputs[0])
    
    return t_node


def setup_metallic(t_node, master_node, n_tree):
    t_node.location = Vector((-600.0, 400.0))
    t_node.image.colorspace_settings.name = 'Non-Color'

    n_tree.links.new(t_node.outputs[0], master_node.inputs[1])


def setup_smoothness(t_node, master_node, n_tree, is_smoothness = True):
    t_node.location = Vector((-600.0, 200.0))
    t_node.image.colorspace_settings.name = 'Non-Color'

    if is_smoothness:
        invert_node = n_tree.nodes.new("ShaderNodeInvert")
        invert_node.location = Vector((-300.0, 250.0))
        n_tree.links.new(t_node.outputs[0], invert_node.inputs[1])
        n_tree.links.new(invert_node.outputs[0], master_node.inputs[2])
    else:
        n_tree.links.new(t_node.outputs[0], master_node.inputs[2])



def setup_maos(t_node, master_node, n_tree):
    t_node.location = Vector((-600.0, 400.0))
    t_node.image.colorspace_settings.name = 'Non-Color'

    s_node = n_tree.nodes.new("ShaderNodeSeparateColor")
    s_node.location = Vector((-300.0, 400.0))

    invert_node = n_tree.nodes.new("ShaderNodeInvert")
    invert_node.location = Vector((-300.0, 250.0))


    n_tree.links.new(t_node.outputs[1], invert_node.inputs[1])
    n_tree.links.new(invert_node.outputs[0], master_node.inputs[2])


    n_tree.links.new(t_node.outputs[0],s_node.inputs[0])

    n_tree.links.new(s_node.outputs[0], master_node.inputs[1])

def setup_normal(t_node, master_node, n_tree, normal_map_format):
    t_node.image.colorspace_settings.name = 'Non-Color'
    t_node.location = Vector((-600.0, 0.0))

    normal_map_node = n_tree.nodes.new("ShaderNodeNormalMap")
    
    
    if normal_map_format == '1':
        normal_map_node.location = Vector((100.0, 0))

        seperate_color = n_tree.nodes.new("ShaderNodeSeparateColor")
        seperate_color.location = Vector((-350.0, 0))

        invert_g = n_tree.nodes.new("ShaderNodeInvert")
        invert_g.location = Vector((-200.0, 0))

        combine_color = n_tree.nodes.new("ShaderNodeCombineColor")
        combine_color.location = Vector((-50.0, 0))

        n_tree.links.new(t_node.outputs[0], seperate_color.inputs[0])
        n_tree.links.new(seperate_color.outputs[0], combine_color.inputs[0])
        n_tree.links.new(seperate_color.outputs[1], invert_g.inputs[1])
        n_tree.links.new(invert_g.outputs[0], combine_color.inputs[1])
        n_tree.links.new(seperate_color.outputs[2], combine_color.inputs[2])
        n_tree.links.new(combine_color.outputs[0], normal_map_node.inputs[1])

    else:
        normal_map_node.location = Vector((-550.0, 0))
        n_tree.links.new(t_node.outputs[0], normal_map_node.inputs[1])

    n_tree.links.new(normal_map_node.outputs[0], master_node.inputs[5])


def setup_height(t_node, master_node, n_tree, o_node):
    t_node.image.colorspace_settings.name = 'Non-Color'
    t_node.location = Vector((-600.0, -350.0))
    
    displacement_node = n_tree.nodes.new("ShaderNodeDisplacement")
    displacement_node.location = Vector((-300.0, -350.0))

    
    n_tree.links.new(t_node.outputs[0], displacement_node.inputs[0])
     
    n_tree.links.new(displacement_node.outputs[0], o_node.inputs[2])
    

def set_color(rgb_node, r, g, b):
    rgb_node.outputs[0].default_value[0] = r
    rgb_node.outputs[0].default_value[1] = g
    rgb_node.outputs[0].default_value[2] = b


def _hf2_pattern_node_group(node_group):
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")
    separate_mask_map = node_group.nodes.new("ShaderNodeSeparateColor")


    color_r = node_group.interface.new_socket("Color R", socket_type = 'NodeSocketColor')
    color_g = node_group.interface.new_socket("Color G", socket_type = 'NodeSocketColor')
    color_b = node_group.interface.new_socket("Color B", socket_type = 'NodeSocketColor')
    color_a = node_group.interface.new_socket("Color A", socket_type = 'NodeSocketColor')
    color_output = node_group.interface.new_socket("Color Output", socket_type = 'NodeSocketColor', in_out = 'OUTPUT')


    color_r.default_value = (1,0,0,1)
    color_g.default_value = (0,1,0,1)
    color_b.default_value = (0,0,1,1)
    color_a.default_value = (0,0,0,1)

    mask_map = node_group.interface.new_socket("Mask Map", socket_type = 'NodeSocketColor')
    mask_map_alpha = node_group.interface.new_socket("Mask Map Alpha", socket_type = 'NodeSocketFloat')
    mask_map_alpha.default_value = 0


    color_map = node_group.interface.new_socket("Color Map", socket_type = 'NodeSocketColor')
    color_map_alpha = node_group.interface.new_socket("Color Map Alpha", socket_type = 'NodeSocketFloat')
    color_map_alpha.default_value = 1

    
    mix_1 = node_group.nodes.new("ShaderNodeMixRGB")
    mix_1.location = Vector((-500.0, 400))
    node_group.links.new(input_node.outputs[0], mix_1.inputs[1])
    node_group.links.new(input_node.outputs[1], mix_1.inputs[2])
    node_group.links.new(separate_mask_map.outputs[1], mix_1.inputs[0])


    mix_2 = node_group.nodes.new("ShaderNodeMixRGB")
    mix_2.location = Vector((-300.0,200))
    node_group.links.new(mix_1.outputs[0], mix_2.inputs[1])
    node_group.links.new(input_node.outputs[2], mix_2.inputs[2])
    node_group.links.new(separate_mask_map.outputs[2], mix_2.inputs[0])

    mix_3 = node_group.nodes.new("ShaderNodeMixRGB")
    mix_3.location = Vector((-100.0,0))
    node_group.links.new(mix_2.outputs[0], mix_3.inputs[1])
    node_group.links.new(input_node.outputs[3], mix_3.inputs[2])
    node_group.links.new(input_node.outputs[5], mix_3.inputs[0])

    mix_4 = node_group.nodes.new("ShaderNodeMixRGB")
    mix_4.location = Vector((100.0,-200))
    node_group.links.new(input_node.outputs[6], mix_4.inputs[1])
    node_group.links.new(input_node.outputs[7], mix_4.inputs[0])
    node_group.links.new(mix_3.outputs[0], mix_4.inputs[2])


    input_node.location = (-1000, 0)
    output_node.location = (1000, 0)

    separate_mask_map.location = (-800,200)
    node_group.links.new(input_node.outputs[4],separate_mask_map.inputs[0])

    node_group.links.new(mix_4.outputs[0],output_node.inputs[0])


def create_color_mix_nodegroup(node_tree):
    if Defaults.HF2PATTERNNODEGROUP not in bpy.data.node_groups:
        nd = bpy.data.node_groups.new(Defaults.HF2PATTERNNODEGROUP, 'ShaderNodeTree')
        _hf2_pattern_node_group(nd)
        
    node_group = bpy.data.node_groups[Defaults.HF2PATTERNNODEGROUP]

    group = node_tree.nodes.new(type='ShaderNodeGroup')
    group.node_tree = node_group

    group.location = (-200, 1000)

    return group


def create_texture_node(material, image, mapping_node):
    t_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    t_node.image = image
    t_node.image.colorspace_settings.name = "sRGB"
    m_node_tree = material.node_tree
    m_node_tree.links.new(mapping_node.outputs[0],t_node.inputs[0])

    return t_node


def create_texture_nodes_standard(material, mtz, master_node, mapping_node,o_node):
    color_mix_nodegroup = None
    if(mtz.mask_map_texture):
        t_node = create_texture_node(material, mtz.mask_map_texture, mapping_node)
        color_mix_nodegroup = create_color_mix_nodegroup(material.node_tree)
        t_node.location = (-600,1200)
        material.node_tree.links.new(t_node.outputs[0],color_mix_nodegroup.inputs[4])
        material.node_tree.links.new(t_node.outputs[1],color_mix_nodegroup.inputs[5])
    
    if(mtz.main_texture):
        t_node = create_texture_node(material, mtz.main_texture, mapping_node)
        setup_albedo(t_node,master_node, material.node_tree, color_mix_nodegroup)

    if(mtz.normal_map_texture):
        t_node = create_texture_node(material, mtz.normal_map_texture, mapping_node)
        setup_normal(t_node,master_node, material.node_tree, mtz.normal_map_format)

    if(mtz.maos_texture_combined == '0'):
        if(mtz.maos_texture):
            t_node = create_texture_node(material, mtz.maos_texture, mapping_node)
            setup_maos(t_node,master_node, material.node_tree)
    else:
        if(mtz.metallic_texture):
            t_node = create_texture_node(material, mtz.metallic_texture, mapping_node)
            setup_metallic(t_node,master_node, material.node_tree)
        if(mtz.smoothness_texture):
            t_node = create_texture_node(material, mtz.smoothness_texture, mapping_node)
            setup_smoothness(t_node,master_node, material.node_tree, mtz.is_smoothness)


def create_texture_nodes_pattern(material, mtz, master_node, mapping_node,o_node):
    if(mtz.normal_map_texture):
        t_node = create_texture_node(material, mtz.normal_map_texture, mapping_node)
        setup_normal(t_node,master_node, material.node_tree)

    color_mix_nodegroup = create_color_mix_nodegroup(material.node_tree)
    material.node_tree.links.new(color_mix_nodegroup.outputs[0],master_node.inputs[0])

    if(mtz.mask_map_texture):
        t_node = create_texture_node(material, mtz.mask_map_texture, mapping_node)
        t_node.location = (-600,1000)
        t_node.image.alpha_mode = "CHANNEL_PACKED"
        material.node_tree.links.new(t_node.outputs[0],color_mix_nodegroup.inputs[4])
        material.node_tree.links.new(t_node.outputs[1],color_mix_nodegroup.inputs[5])

    if(mtz.color_map_texture):
        t_node = create_texture_node(material, mtz.color_map_texture, mapping_node)
        t_node.location = (-600,600)
        t_node.image.alpha_mode = "CHANNEL_PACKED"
        material.node_tree.links.new(t_node.outputs[0],color_mix_nodegroup.inputs[6])
        material.node_tree.links.new(t_node.outputs[1],color_mix_nodegroup.inputs[7])



def create_mapping_node(material, uv_scale):
    m_node_tree = material.node_tree

    m_node = material.node_tree.nodes.new("ShaderNodeMapping")
    m_node.location = Vector((-1200.0, 400.0))
    uv_node = material.node_tree.nodes.new("ShaderNodeTexCoord")
    uv_node.location = Vector((-1400.0, 400.0))

    m_node.inputs[3].default_value[0] = uv_scale
    m_node.inputs[3].default_value[2] = uv_scale
    m_node.inputs[3].default_value[1] = uv_scale

    m_node_tree.links.new(uv_node.outputs[2],m_node.inputs[0])

    return m_node



def reset_material_node_tree(material):
    m_node_tree = material.node_tree
    m_node_tree.nodes.clear()
    
    o_node = m_node_tree.nodes.new("ShaderNodeOutputMaterial")
    o_node.location = Vector((800, 800))
    
    bsdf_node = m_node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf_node.location = Vector((400, 800))

    m_node_tree.links.new(bsdf_node.outputs[0],o_node.inputs[0])
    return o_node

def assign_materializer(material, mtz, is_icon):
    o_node = reset_material_node_tree(material)
    master_node = material.node_tree.nodes["Principled BSDF"]
    uv_scale = 1.0
    if not is_icon:
        uv_scale = float(mtz.uv_unit_sizes[mtz.active_uv_unit_sizes_index].name)
    mapping_node = create_mapping_node(material, uv_scale)

    if int(mtz.type) == 0:
        create_texture_nodes_standard(material, mtz, master_node, mapping_node, o_node)
    if int(mtz.type) == 1:
        create_texture_nodes_pattern(material, mtz, master_node, mapping_node, o_node)