import bpy
from . import ui

class CC_Addon_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("hf2mtz.instal_pillow", text = "Install Pillow", icon = "PACKAGE")


classes = (
    CC_Addon_Preferences,
)	


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    context = bpy.context
    prefs = bpy.context.preferences.addons[__package__].preferences

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)