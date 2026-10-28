import os
from math import radians

import bpy
from bpy.app.handlers import persistent
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

from .hf_data import Enums, MaterializerCategory, PatternCategory
from .hf_data.HelpData import HF2HelpElement
from .consts import Defaults

def is_allowed_texture(image):
    return os.path.splitext(image.filepath)[1].lower() in Defaults.ALLOWEDTEXTUREEXTENSIONS

def _texture_poll(self, image):
    return is_allowed_texture(image)

def _texture_update(prop_name):
    def update(self, context):
        image = getattr(self, prop_name)
        if image is None or is_allowed_texture(image):
            return
        setattr(self, prop_name, None)

        def draw(menu, context):
            menu.layout.label(text = "Only PNG, JPG and JPEG textures are supported.")
        if context.window:
            context.window_manager.popup_menu(draw, title = "Unsupported texture \"%s\"" % image.name, icon = 'ERROR')
    return update

def texture_property(prop_name):
    return PointerProperty(type = bpy.types.Image, poll = _texture_poll, update = _texture_update(prop_name))

def get_mtz_categories(mtz_type):
    if mtz_type == '1':
        return PatternCategory.categories
    return MaterializerCategory.categories

def category_fits_mtz_type(category, mtz_type):
    main_cat, _, subcat = category.strip().partition("/")
    subcats = get_mtz_categories(mtz_type).get(main_cat)
    if subcats is None:
        return False
    return not subcat or subcat in subcats

def _mtz_type_update(self, context):
    if self.materializer_category and not category_fits_mtz_type(self.materializer_category, self.type):
        self.materializer_category = ""


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
    override_price : BoolProperty(default = False, description = HF2HelpElement.ArticleOverridePrice.value)
    price : IntProperty(default = 0, min = 0, description = HF2HelpElement.ArticlePrice.value)
    shop_category : StringProperty(default = "")

    item_kind : StringProperty(default = "")
    item_kind_is_custom : BoolProperty(default = False)

    item_series : StringProperty(default = "")
    item_series_is_custom : BoolProperty(default = False)

    affordability : StringProperty(default = "")

    x_factor : IntProperty(default = 0, options = {'HIDDEN'})



class HF2_Materializer(bpy.types.PropertyGroup):
    display_name : StringProperty(default = "Display Name", description = HF2HelpElement.MaterializerName.value)
    type : EnumProperty(items = Enums.mtz_type, description = HF2HelpElement.MaterializerType.value, update = _mtz_type_update)
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


    main_texture : texture_property("main_texture")
    normal_map_texture : texture_property("normal_map_texture")
    normal_map_format : EnumProperty(items = [('0', "OpenGL", ""), ('1', "DirectX", "")], default = '0', description = HF2HelpElement.NormalMapFormat.value)


    maos_texture : texture_property("maos_texture")
    maos_texture_combined :  EnumProperty(items = [('0', "Combined", ""), ('1', "Split", "")], default = '0', description = HF2HelpElement.MAOSTextureType.value)


    ao_texture : texture_property("ao_texture")
    smoothness_texture : texture_property("smoothness_texture")
    is_smoothness : BoolProperty(default = True, description = HF2HelpElement.UseSmoothnessInsteadOfRoughness.value)
    metallic_texture : texture_property("metallic_texture")



    height_texture : texture_property("height_texture")
    height_blend_texture : PointerProperty(type = bpy.types.Texture)

    icon_texture : texture_property("icon_texture")

    color_map_texture : texture_property("color_map_texture")
    mask_map_texture : texture_property("mask_map_texture")
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
