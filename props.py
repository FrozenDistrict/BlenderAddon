from math import radians

import bpy
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

from .hf_data import Enums
from .hf_data.HelpData import HF2HelpElement


def get_HF2_Mtz_props():
    return bpy.context.scene.hf2Mtz

def get_HF2_Mtz_list():
    return get_HF2_Mtz_props().hf2_materializers

def get_HF2_Active_Mtz():
    return get_HF2_Mtz_list()[get_HF2_Mtz_props().active_mtz_index]


class HF2_Selectable_Element(bpy.types.PropertyGroup):
    element_name: StringProperty(name = "", default = "")
    ID: IntProperty()
    selected: BoolProperty(name = "Is Selected", default = False)


class HF2_List(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(default = "")
    value : bpy.props.IntProperty(default = 1)



class HF2_Article_Data(bpy.types.PropertyGroup):
    price : IntProperty(default = 0, min = 0, description = HF2HelpElement.ArticlePrice.value)
    shop_category : StringProperty(default = "")

    item_kind : StringProperty(default = "")
    item_kind_is_custom : BoolProperty(default = False)

    item_series : StringProperty(default = "")
    item_series_is_custom : BoolProperty(default = False)

    affordability : StringProperty(default = "")

    x_factor : IntProperty(default = 0, options = {'HIDDEN'})



class HF2_Materializer(bpy.types.PropertyGroup):
    name : StringProperty(default = "Name", description = HF2HelpElement.MaterializerName.value)
    type : EnumProperty(items = Enums.mtz_type, description = HF2HelpElement.MaterializerType.value)
    custom_colors : IntProperty(default = 0, soft_min = 0, soft_max = 4, description = HF2HelpElement.CustomColors.value)
    avaliability : EnumProperty(items = Enums.avaliability, description = HF2HelpElement.Avaliability.value)
    category :  IntProperty(default = 0)

    mod_path : StringProperty(name = "Mod Path", default = "", description = HF2HelpElement.ModPath.value, maxlen=2000,
        subtype='DIR_PATH')

    materializer_stid : StringProperty()
    materializer_category : StringProperty()
    active_mtz_stid_index : IntProperty(default = 0)


    uv_unit_sizes : CollectionProperty(type = HF2_List)
    active_uv_unit_sizes_index : IntProperty(default = 0)

    is_grimy : BoolProperty(default = False, description = HF2HelpElement.IsGrimy.value)
    support_mosaic : BoolProperty(default = False, description = HF2HelpElement.SupportMosaic.value)
    support_pattern : BoolProperty(default = False, description = HF2HelpElement.SupportPattern.value)


    main_texture : PointerProperty(type = bpy.types.Image)
    normal_map_texture : PointerProperty(type = bpy.types.Image)
    normal_map_format : EnumProperty(items = [('0', "OpenGL", ""), ('1', "DirectX", "")], default = '0', description = HF2HelpElement.NormalMapFormat.value)


    maos_texture : PointerProperty(type = bpy.types.Image)
    maos_texture_combined :  EnumProperty(items = [('0', "Combined", ""), ('1', "Split", "")], default = '0', description = HF2HelpElement.MAOSTextureType.value)


    ao_texture : PointerProperty(type = bpy.types.Image)
    smoothness_texture : PointerProperty(type = bpy.types.Image)
    is_smoothness : BoolProperty(default = True, description = HF2HelpElement.UseSmoothnessInsteadOfRoughness.value)
    metallic_texture : PointerProperty(type = bpy.types.Image)



    height_texture : PointerProperty(type = bpy.types.Image)
    height_blend_texture : PointerProperty(type = bpy.types.Texture)

    icon_texture : PointerProperty(type = bpy.types.Image)

    color_map_texture : PointerProperty(type = bpy.types.Image)
    mask_map_texture : PointerProperty(type = bpy.types.Image)
    invert_mask_alpha : BoolProperty(default = False, description = HF2HelpElement.InvertAlpha.value)

    allowed_rotations : EnumProperty(items = Enums.allowed_rotations, description = HF2HelpElement.AllowedRotations.value)
    pattern_usage : EnumProperty(items = Enums.pattern_usage, description = HF2HelpElement.PatternUsage.value)

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

    bpy.types.Scene.hf2Mtz = PointerProperty(type=CC_Addon_Props)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.hf2Mtz
