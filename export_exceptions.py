class UVScaleWrongFormat(Exception):
    def __init__(self,e):
        super().__init__(f"\"{e.name}\" - UV Unit Size is invalid!  Be sure to set it to float value e.g. 1.5")

class HF2ModFolderInvalid(Exception):
    def __init__(self,e):
        super().__init__(f"{e} - mod folder path is invalid! Set it to correct folder!")

class EmptyData(Exception):
    def __init__(self,e):
        super().__init__(f"{e} is empty!")

class NoMTZ(Exception):
    def __init__(self,e):
        super().__init__(f"There is no selected Materializer for export!")

class NoPO2(Exception):
    def __init__(self,e):
        super().__init__(f"{e} texture is not power of 2! Make sure all textures are PO2! E.g. 512x512, 1024x1024, 2048x2048 etc.")

class UnsupportedTextureFormat(Exception):
    def __init__(self,e):
        super().__init__(f"{e} texture has unsupported format! Only PNG, JPG and JPEG textures are supported.")

class TextureUnreadable(Exception):
    def __init__(self,e):
        super().__init__(f"{e} texture could not be read! Make sure the image file exists and is a valid image.")

class PillowNotInstalled(Exception):
    def __init__(self):
        super().__init__(f"Pillow package is not installed! Please install it using button in addon preferences.")

class PillowInstallationError(Exception):
    def __init__(self):
        super().__init__(f"Can't install Pillow package! Please install it manually using pip.")

class SplitTexturesNotSameSize(Exception):
    def __init__(self):
        super().__init__(f"Split MAOS textures are not the same size! Please make sure all assigned textures have the same dimensions.")