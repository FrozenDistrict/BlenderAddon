import bpy
import importlib.metadata
import sys
import subprocess
from .hf_data.HelpData import HF2HelpElement
from .export_exceptions import PillowInstallationError


def get_pillow_version():
    try:
        return importlib.metadata.version("Pillow")
    except importlib.metadata.PackageNotFoundError:
        return None

def install_pillow(upgrade = False):
    print("Installing Pillow...")
    path = bpy.utils.user_resource("SCRIPTS", path="modules")
    upgrade_args = ["--upgrade"] if upgrade else []
    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "--target", path] + upgrade_args)
    except subprocess.CalledProcessError:
        raise PillowInstallationError()

    # Blender only adds the modules folder to sys.path at startup if it already existed
    if path not in sys.path:
        sys.path.append(path)
    importlib.invalidate_caches()
    print("Pillow installed successfully")

def ensure_pillow_installed():
    if get_pillow_version() is None:
        install_pillow()
    else:
        print("Pillow already installed")


class HF2_MTZ_OP_InstallPillow(bpy.types.Operator):
    bl_idname = "hf2mtz.instal_pillow"
    bl_label = "Install pillow package"
    bl_options = {'REGISTER'}
    bl_description = HF2HelpElement.InstallPillow.value

    upgrade : bpy.props.BoolProperty(default = False)
    
    def execute(self, context):
        try:
            install_pillow(self.upgrade)
        except Exception as err:
            self.report({"ERROR"}, err.__str__())
            return {"CANCELLED"}
        message = "Pillow %s installed!" % get_pillow_version()
        if self.upgrade:
            message += " Restart Blender to use it."
        self.report({"INFO"}, message)
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
