import bpy
from .module_install import get_pillow_version

class CC_Addon_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        version = get_pillow_version()
        if version:
            row.label(text = "Pillow installed (%s)" % version, icon = "CHECKMARK")
            layout.operator("hf2mtz.instal_pillow", text = "Update Pillow", icon = "FILE_REFRESH").upgrade = True
        else:
            row.operator("hf2mtz.instal_pillow", text = "Install Pillow", icon = "PACKAGE")


classes = (
    CC_Addon_Preferences,
)	


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)