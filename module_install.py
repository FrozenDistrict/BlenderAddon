import bpy
import importlib.util
import sys
import subprocess
from .hf_data.HelpData import HF2HelpElement


def ensure_pillow_installed():
    if importlib.util.find_spec("PIL") is None:
        print("Pillow not found. Installing...")
        path = bpy.utils.user_resource("SCRIPTS", path="MODULES")
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "--target", path])
        print("Pillow installed successfully")
    else:
        print("Pillow already installed")


class HF2_MTZ_OP_InstallPillow(bpy.types.Operator):
    bl_idname = "hf2mtz.instal_pillow"
    bl_label = "Install pillow package"
    bl_options = {'REGISTER'}
    bl_description = HF2HelpElement.InstallPillow.value
    
    def execute(self, context):
        ensure_pillow_installed()

        return {'FINISHED'}
    


classes = (
    HF2_MTZ_OP_InstallPillow,
)	


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
