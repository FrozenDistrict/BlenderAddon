import bpy

from bpy.types import Menu
from .hf_data.HelpData import HF2HelpElement
from .hf_data.MaterializerCategory import categories
from .hf_data.MaterializerTypes import MtzTypes

class HF2_Subpanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "HF2"
    bl_options = {"DEFAULT_CLOSED"}


class HF2_UI_LIST_A(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        slot = item

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if slot:
                layout.prop(slot, "name", text="", emboss=False, icon_value=icon)
            else:
                layout.label(text="", translate=False, icon_value=icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class HF2_UI_LIST_B(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        slot = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if slot:
                layout.label( text=slot.name,  icon_value=icon)

            else:
                layout.label(text="", translate=False, icon_value=icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class HF2_MTZ_PT_Main(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "HF2 Surfacers"
    bl_idname = "HF2_MTZ_PT_toolbox_panel"
    bl_category = "HF2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        scn = context.scene.hf2Mtz

        layout.template_list("HF2_UI_LIST_A", "Mtz List", scn, "hf2_materializers", scn, "active_mtz_index")

        row = layout.row()
        row.operator("hf2mtz.create_mtz", text = "Add Surfacer", icon = "ADD")        
        row.operator("hf2mtz.remove_mtz", text = "Remove Surfacer", icon = "REMOVE")        

        row = layout.row()
        row.scale_y = 2
        row.operator("hf2mtz.export_materializer", text = "Export Selected", icon = "PACKAGE")


class HF2_MTZ_PT_Mtz_Preview_Settings(HF2_Subpanel,bpy.types.Panel):
    bl_parent_id = "HF2_MTZ_PT_toolbox_panel"
    bl_label = "Final Settings"

    def draw(self, context):
        layout = self.layout
        scn = context.scene.hf2Mtz
        if len(scn.hf2_materializers) == 0:
            return
        mtz = scn.hf2_materializers[scn.active_mtz_index]
        row = layout.row()
        row.operator("hf2mtz.setup_preview_collection", text = "Setup icon render scene", icon = "GROUP")

        row = layout.row()
        row.operator("hf2mtz.render_icon", text = "Render Icon", icon = "IMAGE")

        draw_texture(layout, "Icon:", mtz, "icon_texture")



class HF2_MTZ_PT_Mtz_Article_Data(HF2_Subpanel,bpy.types.Panel):
    bl_parent_id = "HF2_MTZ_PT_toolbox_panel"
    bl_label = "Article Data"

    def draw(self, context):
        layout = self.layout
        scn = context.scene.hf2Mtz
        if len(scn.hf2_materializers) == 0:
            return
        mtz = scn.hf2_materializers[scn.active_mtz_index]
        row = layout.row()

        article_data = mtz.article_data

        row = layout.row()
        row.label(text = "Shop Category:")
        if article_data.shop_category:
            row.operator("hf2mtz.article_select_shop_category", text = article_data.shop_category)
        else:
            row.operator("hf2mtz.article_select_shop_category", text = "Select Shop Category")


        layout = layout.box()
        if article_data.shop_category == "" or article_data.shop_category == "None":
            layout.active = False
    
        row = layout.row()
        row.prop(article_data, "override_price", text = "Override Price")

        if article_data.override_price:
            row = layout.row()
            row.prop(article_data, "price", text = "Price")

        row = layout.row()
        row.label(text = "Item Kind:")
        row.scale_x = 0.5
        row.prop(article_data, "item_kind_is_custom", text = "Custom")
        row = layout.row()
        if article_data.item_kind_is_custom:
            row.prop(article_data, "item_kind", text = "")
        else:
            if article_data.item_kind:
                row.operator("hf2mtz.article_select_item_kind", text = article_data.item_kind)
            else:
                row.operator("hf2mtz.article_select_item_kind", text = "Select")


        layout.separator()

        row = layout.row()
        row.label(text = "Item Series:")
        row.scale_x = 0.5
        row.prop(article_data, "item_series_is_custom", text = "Custom")
        row = layout.row()
        if article_data.item_series_is_custom:
            row.prop(article_data, "item_series", text = "")
        else:
            if article_data.item_series:
                row.operator("hf2mtz.article_select_item_series", text = article_data.item_series)
            else:
                row.operator("hf2mtz.article_select_item_series", text = "Select")
            

        row = layout.row()
        row.label(text = "Affordability:")
        if article_data.affordability:
            row.operator("hf2mtz.article_select_affordability", text = article_data.affordability)
        else:
            row.operator("hf2mtz.article_select_affordability", text = "Select")
        
     


class HF2_MTZ_PT_Mtz_Settings_General(HF2_Subpanel,bpy.types.Panel):
    bl_parent_id = "HF2_MTZ_PT_toolbox_panel"
    bl_label = "Texture Settings"


    def draw(self, context):
        layout = self.layout
        scn = context.scene.hf2Mtz
        if len(scn.hf2_materializers) == 0:
            return
        mtz = scn.hf2_materializers[scn.active_mtz_index]
        row = layout.row()

        if mtz.type == '0':
            draw_textures_settings(self, layout, mtz)

        if int(mtz.type) == 0:
            draw_textures_standard(self, layout, mtz)
        if int(mtz.type) == 1:
            draw_textures_pattern(self, layout, mtz)
      

def draw_textures_settings(self, layout, mtz):
    box = layout.box()
    row = box.row()
    row.prop(mtz, "maos_texture_combined", text = "MAOS Texture Type")
    row = box.row()
    if mtz.maos_texture_combined == '1':
        row.enabled = True
        row.prop(mtz, "is_smoothness", text = "Use Smoothness Instead Of Roughness")
    else:
        row.enabled = False
        row.prop(mtz, "is_smoothness", text = "Use Smoothness Instead Of Roughness")

def draw_textures_standard(self, layout, mtz):
    draw_texture(layout, "Basecolor:", mtz, "main_texture")


    box = layout.box()
    row = box.row()
    draw_texture(box, "Normal map:", mtz, "normal_map_texture")
    row.prop(mtz, "normal_map_format", text = "Format")


    if mtz.maos_texture_combined == '0':
        draw_texture(layout, "MAOS: (R - Metallic, G - AO, S - Smoothness)", mtz, "maos_texture")
    else:
        draw_texture(layout, "Metallic:", mtz, "metallic_texture")
        draw_texture(layout, "AO:", mtz, "ao_texture")

        if mtz.is_smoothness:
            draw_texture(layout, "Smoothness:", mtz, "smoothness_texture")
        else:
            draw_texture(layout, "Roughness:", mtz, "smoothness_texture")

    draw_texture(layout, "Height map:", mtz, "height_texture")

    box = layout.box()
    draw_texture(box, "Mask Map", mtz, "mask_map_texture")
    row = box.row()
    
    row.label(text = "Set Alpha To 0")
    row.prop(mtz, "invert_mask_alpha", text = "")

def draw_textures_pattern(self, layout, mtz):
    draw_texture(layout, "Color Map:", mtz, "color_map_texture")
    draw_texture(layout, "Normal map: (OpenGL Format)", mtz, "normal_map_texture")
    box = layout.box()
    draw_texture(box, "Mask Map", mtz, "mask_map_texture")
    row = box.row()
    row.label(text = "Set Alpha To 0")
    row.prop(mtz, "invert_mask_alpha", text = "")

def draw_texture(layout, label, mtz, texture_prop):
    row = layout.row()
    row.label(text= label)
    row = layout.row()
    row.template_ID_preview(mtz, texture_prop, open="image.open", rows=2, cols=2)



class HF2_MTZ_PT_Mtz_Settings_Textures(HF2_Subpanel,bpy.types.Panel):
    bl_parent_id = "HF2_MTZ_PT_toolbox_panel"
    bl_label = "General Settings"

    def draw(self, context):
        layout = self.layout
        scn = context.scene.hf2Mtz
        if len(scn.hf2_materializers) == 0:
            return
        mtz = scn.hf2_materializers[scn.active_mtz_index]

        row = layout.row()
        row.prop(mtz,"mod_path", text = "Mod Path")

        row = layout.row()
        row.prop(mtz,"name", text = "Name")

        row = layout.row()
        row.label(text = "Category:")
        if mtz.materializer_category:
            row.operator("hf2mtz.select_mtz_category_dialog", text = mtz.materializer_category)
        else:
            row.operator("hf2mtz.select_mtz_category_dialog", text = "Select")

        row = layout.row()
        row.label(text="Tag:")
        if mtz.materializer_stid:
            row.operator("hf2mtz.select_mtz_stid_dialog", text = mtz.materializer_stid)
        else:
            row.operator("hf2mtz.select_mtz_stid_dialog", text = "Select")
    


        row = layout.row()
        row.prop(mtz,"type", text = "Type")

        row = layout.row()
        row.prop(mtz,"custom_colors", text = "Custom colors")
        

        uvBox = layout.box()

        row = uvBox.row()
        row.label(text= "UV Sizes")
        draw_help(row, HF2HelpElement.UVUnitSizes)
        
        row = uvBox.row()
        row.operator("hf2mtz.add_unit_size", text = "Add", icon = "ADD")    
        row.operator("hf2mtz.remove_unit_size", text = "Remove", icon = "REMOVE")    
            
        uvBox.template_list("HF2_UI_LIST_A", "UV Unit List", mtz, "uv_unit_sizes", mtz, "active_uv_unit_sizes_index")

        row = layout.row()
        row.prop(mtz,"avaliability", text = "Avaliability")
        row = layout.row()
        row.prop(mtz, "allowed_rotations", text = "Allowed Rotations")

        if int(mtz.type) == 0:
            draw_toggles_standard(self, layout, mtz)
        if int(mtz.type) == 1:
            draw_toggles_pattern(self, layout, mtz)

   


def draw_toggles_standard(self, layout, mtz):
    box = layout.box()
    row = box.row()
    row.prop(mtz, "is_grimy", text = "Is Damaged")
    row = box.row()
    row.prop(mtz, "support_mosaic", text = "Support Cut Pattern")
    row = box.row()
    row.prop(mtz, "support_pattern", text = "Is colorable by Pattern")



def draw_toggles_pattern(self, layout, mtz):
    box = layout.box()
    row = box.row()
    row.prop(mtz, "pattern_usage", text = "Pattern usage")





def draw_help(row, hf2_help_element):
    row.operator("hf2mtz.show_help", text = "",icon = "HELP").element = hf2_help_element.value

def draw_category_iter(layout, category, enabled_category):

    for key, subcat in category.items():
        layout.separator()
        if subcat:
            box = layout.box()
            row = box.row()
            row.operator("hf2mtz.select_mtz_category", text = key, depress = key == enabled_category, icon = 'FILE_FOLDER').category_stid = key

            for subkey in subcat.keys():
                text = "    %s/%s" % (key, subkey)
                box.operator("hf2mtz.select_mtz_category", text = text, depress = text == enabled_category, icon = 'FILE_FOLDER').category_stid = text
        else:
            layout.operator("hf2mtz.select_mtz_category", text = key, depress = key == enabled_category, icon = 'FILE_FOLDER',).category_stid = key

def draw_categories(layout, categories, enabled_category):
    col = layout.column(align=True)
        
    grid = col.grid_flow(columns=3, even_columns=True, even_rows=False)
        
    for main_cat, subcats in categories.items():
        box = grid.box()
        
        if subcats:
            for subcat in subcats.keys():
                text = "    %s/%s" % (main_cat, subcat)
                box.operator("hf2mtz.select_mtz_category", text = text, depress = text == enabled_category, icon = 'DOT').category_stid = text
        else:
            box.operator("hf2mtz.select_mtz_category", text = main_cat, depress = main_cat == enabled_category, icon = 'DOT').category_stid = main_cat
            

def draw_stids(layout, categories, enabled_category):
    col = layout.column(align=True)
        
    grid = col.grid_flow(columns=3, even_columns=True, even_rows=False)
        
    for main_cat in categories:
        box = grid.row()
        box.operator("hf2mtz.set_mtz_stid", text = main_cat, depress = main_cat == enabled_category, icon = 'DOT').mtz_stid = main_cat
        


def categories_dialog(self, context):
    layout = self.layout
    layout.ui_units_x = 40
    row = layout.row()
    scn = context.scene.hf2Mtz
    mtz = scn.hf2_materializers[scn.active_mtz_index]
    enabled_category = mtz.materializer_category

    draw_categories(layout, categories, enabled_category)


def mtz_stids_dialog(self, context):
    layout = self.layout
    layout.ui_units_x = 40
    row = layout.row()
    scn = context.scene.hf2Mtz
    mtz = scn.hf2_materializers[scn.active_mtz_index]
    enabled_category = mtz.materializer_stid

    draw_stids(layout, MtzTypes, enabled_category)
        


classes = (
    HF2_UI_LIST_A,
    HF2_UI_LIST_B,

    HF2_MTZ_PT_Main,
    HF2_MTZ_PT_Mtz_Settings_Textures,
    HF2_MTZ_PT_Mtz_Settings_General,
    HF2_MTZ_PT_Mtz_Preview_Settings,
    HF2_MTZ_PT_Mtz_Article_Data,

)	


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)