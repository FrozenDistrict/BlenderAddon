import bpy

from .utils import *
from .ui import categories_dialog, mtz_stids_dialog
from .props import HF2_Selectable_Element
from .hf_data.HelpData import HF2HelpElement
from .data_loader import load_tags

class HF2_MTZ_OP_CreateMtz(bpy.types.Operator):
    bl_idname = "hf2mtz.create_mtz"
    bl_label = "Create new Materializer"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = HF2HelpElement.AddMtz.value


    def execute(self, context):
        create_mtz()
        return {'FINISHED'}


class HF2_MTZ_OP_SelectCategory(bpy.types.Operator):
    bl_idname = "hf2mtz.select_mtz_category"
    bl_label = "Select materializer category"
    bl_options = {'INTERNAL','REGISTER', 'UNDO'}
    
    category_stid : bpy.props.StringProperty()
    
    def execute(self, context):
        set_mtz_category(self.category_stid)    
        return {'FINISHED'}

class HF2_MTZ_OP_SelectCategoryDialog(bpy.types.Operator):
    bl_idname = "hf2mtz.select_mtz_category_dialog"
    bl_label = "Select materializer category dialog"
    bl_options = {'INTERNAL'}
    bl_description = HF2HelpElement.MaterializerCategory.value
    

    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_props_dialog(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        categories_dialog(self,context)


class HF2_MTZ_OP_RemoveMtz(bpy.types.Operator):
    bl_idname = "hf2mtz.remove_mtz"
    bl_label = "Remove Materializer"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = HF2HelpElement.DeleteMtz.value
    

    def execute(self, context):
        remove_mtz()
        return {'FINISHED'}


class HF2_MTZ_OP_AddUvSize(bpy.types.Operator):
    bl_idname = "hf2mtz.add_unit_size"
    bl_label = "Add uv unit size to materializer"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = HF2HelpElement.AddUvsizes.value


    def execute(self, context):
        add_uv_unit_size()
        return {'FINISHED'}

class HF2_MTZ_OP_RemoveUvSize(bpy.types.Operator):
    bl_idname = "hf2mtz.remove_unit_size"
    bl_label = "Remove uv unit size to materializer"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = HF2HelpElement.RemoveUvsizes.value


    def execute(self, context):
        remove_un_unit_size()
        return {'FINISHED'}
    
class HF2_MTZ_OP_SelectMtzStidDialog(bpy.types.Operator):
    bl_idname = "hf2mtz.select_mtz_stid_dialog"
    bl_label = "Select materializer stid dialog"
    bl_options = {'INTERNAL'}
    bl_description = HF2HelpElement.MaterializerStid.value
    

    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_props_dialog(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        mtz_stids_dialog(self,context)



class HF2_MTZ_OP_SetMtzStid(bpy.types.Operator):
    bl_idname = "hf2mtz.set_mtz_stid"
    bl_label = "Set Materializer stid"
    bl_options = {'INTERNAL','REGISTER', 'UNDO'}
    
    mtz_stid : bpy.props.StringProperty()
    
    def execute(self, context):
        set_mtz_stid(self.mtz_stid)    
        return {'FINISHED'}

class HF2_MTZ_OP_SetupPreviewCollection(bpy.types.Operator):
    bl_idname = "hf2mtz.setup_preview_collection"
    bl_label = "Setup preview collection"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = HF2HelpElement.PreviewScene.value

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def execute(self, context):
        setup_preview_main()
        return {'FINISHED'}

class HF2_MTZ_OP_RenderIcon(bpy.types.Operator):
    bl_idname = "hf2mtz.render_icon"
    bl_label = "Render Materializer Icon"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = HF2HelpElement.RenderIcon.value

    @classmethod
    def poll(cls, context):
        return icon_can_be_rendered()

    def execute(self, context):
        try:
            render_icon_preview()
        except Exception as err:
            self.report({"ERROR"}, err.__str__())
            return {"CANCELLED"}
        return {'FINISHED'}


class HF2_MTZ_OP_SetupMaterial(bpy.types.Operator):
    bl_idname = "hf2mtz.setup_preview_material"
    bl_label = "Setup preview material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        return {'FINISHED'}


class HF2_MTZ_OP_ExportMaterializer(bpy.types.Operator):
    bl_idname = "hf2mtz.export_materializer"
    bl_label = "Export materializer"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = HF2HelpElement.ExportMaterializer.value

    def execute(self, context):
        try:
            export_materializer()
        except Exception as err:
            self.report({"ERROR"}, err.__str__())
            return {"CANCELLED"}
        self.report({"INFO"}, "Materializer exported!")
        return {'FINISHED'}
    

class HF2_MTZ_OP_Help(bpy.types.Operator):
    bl_idname = "hf2mtz.show_help"
    bl_label = "Help"
    bl_options = {'INTERNAL'}
    bl_description = "Show help for selected element"

    element : bpy.props.StringProperty(default = "")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return popup_invoke(self, context)

    def draw(self, context):
        l = self.layout
        r = l.row()
        r.label(text = self.element)
    



############## Article data operators #####################

class HF2_MTZ_OP_ArticleSelectItemKind(bpy.types.Operator):
    bl_idname = "hf2mtz.article_select_item_kind"
    bl_label = "Select item kind"
    bl_options = {'INTERNAL','REGISTER', 'UNDO'}
    bl_property = "item_kind"
    bl_description = HF2HelpElement.ArticleItemKind.value

    item_kind : bpy.props.EnumProperty(items = load_tags("item_kind"), description = HF2HelpElement.ArticleItemKind.value)
    
    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        set_mtz_item_kind(self.item_kind)

        return {"FINISHED"}


class HF2_MTZ_OP_ArticleSelectItemSeries(bpy.types.Operator):
    bl_idname = "hf2mtz.article_select_item_series"
    bl_label = "Select item series"
    bl_options = {'INTERNAL','REGISTER', 'UNDO'}
    bl_property = "item_series"
    bl_description = HF2HelpElement.ArticleItemSeries.value

    item_series : bpy.props.EnumProperty(items = load_tags("item_series"), description = HF2HelpElement.ArticleItemSeries.value)
    
    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


    def execute(self, context):
        set_mtz_item_series(self.item_series)    
        return {'FINISHED'}


class HF2_MTZ_OP_ArticleSelectAffordability(bpy.types.Operator):
    bl_idname = "hf2mtz.article_select_affordability"
    bl_label = "Select affordability"
    bl_options = {'INTERNAL','REGISTER', 'UNDO'}
    bl_property = "affordability"
    bl_description = HF2HelpElement.ArticleAffordability.value

    affordability : bpy.props.EnumProperty(items = load_tags("item_tag", "Money/"))

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        set_mtz_affordability(self.affordability)    
        return {'FINISHED'}
    


class HF2_MTZ_OP_ArticleSelectShopCategory(bpy.types.Operator):
    bl_idname = "hf2mtz.article_select_shop_category"
    bl_label = "Select shop category"
    bl_options = {'INTERNAL','REGISTER', 'UNDO'}
    bl_property = "shop_category"
    bl_description = HF2HelpElement.ArticleShopCategory.value
    
    shop_category : bpy.props.EnumProperty(items = load_tags("item_category", "Surface finishes/"))
    
    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


    def execute(self, context):
        set_mtz_shop_category(self.shop_category)    
        return {'FINISHED'}





def popup_invoke(self, context):
    wm = context.window_manager
    dpi = context.preferences.system.pixel_size
    ui_size = context.preferences.system.ui_scale
    dialog_size = 450 * dpi * ui_size

    return wm.invoke_props_dialog(self,  width=int(dialog_size))


classes = (
    HF2_MTZ_OP_CreateMtz,
    HF2_MTZ_OP_RemoveMtz,
    HF2_MTZ_OP_AddUvSize,
    HF2_MTZ_OP_RemoveUvSize,
    HF2_MTZ_OP_SetupPreviewCollection,
    HF2_MTZ_OP_ExportMaterializer,
    HF2_MTZ_OP_SetMtzStid,
    HF2_MTZ_OP_SelectMtzStidDialog,
    HF2_MTZ_OP_RenderIcon,
    HF2_MTZ_OP_Help,
    HF2_MTZ_OP_SelectCategory,
    HF2_MTZ_OP_SelectCategoryDialog,
    HF2_MTZ_OP_ArticleSelectItemKind,
    HF2_MTZ_OP_ArticleSelectItemSeries,
    HF2_MTZ_OP_ArticleSelectAffordability,
    HF2_MTZ_OP_ArticleSelectShopCategory,
)	


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)