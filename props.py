from math import radians
from .hf_data import Enums
import bpy
from .hf_data.HelpData import help_element 


def HF2_Mtz_props():
    return bpy.context.scene.hf2Mtz

def HF2_Mtz_list():
    return HF2_Mtz_props().hf2_materializers

def HF2_Active_Mtz():
    return HF2_Mtz_list()[HF2_Mtz_props().active_mtz_index]

from bpy.props import (
        StringProperty,
        EnumProperty,
        BoolProperty,
        PointerProperty,
        IntProperty,
        CollectionProperty,
        FloatVectorProperty,
        FloatProperty
        )


class HF2_Selectable_Element(bpy.types.PropertyGroup):
    element_name: StringProperty(name = "", default = "")
    ID: IntProperty()
    selected: BoolProperty(name = "Is Selected", default = False)


class HF2_List(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(default = "")
    value : bpy.props.IntProperty(default = 1)



class HF2_Article_Data(bpy.types.PropertyGroup):
    price : IntProperty(default = 0, min = 0, description = help_element(25))
    shop_category : StringProperty(default = "")

    item_kind : StringProperty(default = "")
    item_kind_is_custom : BoolProperty(default = False)
    
    item_series : StringProperty(default = "")
    item_series_is_custom : BoolProperty(default = False)

    affordability : StringProperty(default = "")
    


class HF2_Materializer(bpy.types.PropertyGroup):
    name : StringProperty(default = "Name", description = help_element(19))
    type : EnumProperty(items = Enums.mtz_type, description = help_element(18))
    custom_colors : IntProperty(default = 0, soft_min = 0, soft_max = 4, description = help_element(2))
    avaliability : EnumProperty(items = Enums.avaliability, description = help_element(6))
    category :  IntProperty(default = 0)
    
    mod_path : StringProperty(name = "Mod Path", default = "", description = help_element(20), maxlen=2000,
        subtype='DIR_PATH')

    materializer_stid : StringProperty()
    materializer_category : StringProperty()
    active_mtz_stid_index : IntProperty(default = 0)

    
    uv_unit_sizes : CollectionProperty(type = HF2_List)
    active_uv_unit_sizes_index : IntProperty(default = 0)
    
    is_grimy : BoolProperty(default = False, description = help_element(5))
    support_mosaic : BoolProperty(default = False, description = help_element(3))
    support_pattern : BoolProperty(default = False, description = help_element(4))


    main_texture : PointerProperty(type = bpy.types.Image)
    normal_map_texture : PointerProperty(type = bpy.types.Image)
    normal_map_format : EnumProperty(items = [('0', "OpenGL", ""), ('1', "DirectX", "")], default = '0', description = help_element(24))


    maos_texture : PointerProperty(type = bpy.types.Image)
    maos_texture_combined :  EnumProperty(items = [('0', "Combined", ""), ('1', "Split", "")], default = '0', description = help_element(22))
    

    ao_texture : PointerProperty(type = bpy.types.Image)
    smoothness_texture : PointerProperty(type = bpy.types.Image)
    is_smoothness : BoolProperty(default = True, description = help_element(23))
    metallic_texture : PointerProperty(type = bpy.types.Image)



    height_texture : PointerProperty(type = bpy.types.Image)
    height_blend_texture : PointerProperty(type = bpy.types.Texture)

    icon_texture : PointerProperty(type = bpy.types.Image)

    color_map_texture : PointerProperty(type = bpy.types.Image)
    mask_map_texture : PointerProperty(type = bpy.types.Image)
    invert_mask_alpha : BoolProperty(default = False, description = help_element(9))

    allowed_rotations : EnumProperty(items = Enums.allowed_rotations, description = help_element(14))
    pattern_usage : EnumProperty(items = Enums.pattern_usage, description = help_element(15))

    collection_preview : PointerProperty(type = bpy.types.Collection)
    material_preview : PointerProperty(type = bpy.types.Material)
    material_icon_preview : PointerProperty(type = bpy.types.Material)
    object_preview : PointerProperty(type = bpy.types.Object)
    sun_preview : PointerProperty(type = bpy.types.Object)


    article_data : PointerProperty(type = HF2_Article_Data)
    


class CC_Addon_Props(bpy.types.PropertyGroup):
    hf2_materializers : CollectionProperty(type = HF2_Materializer)
    active_mtz_index : IntProperty(default = 0)
    icon_render_camera : PointerProperty(type = bpy.types.Object)


classes = (
    HF2_List,
    HF2_Article_Data,
    HF2_Materializer,
    HF2_Selectable_Element,
    CC_Addon_Props
)	



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    s = bpy.types.Scene
    m = bpy.types.Material
    o = bpy.types.Object

    s.hf2Mtz = PointerProperty(type=CC_Addon_Props)
    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    s = bpy.types.Scene
    m = bpy.types.Material
    o = bpy.types.Object

    del s.hf2Mtz
    