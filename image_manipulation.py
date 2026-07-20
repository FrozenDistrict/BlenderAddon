import os
import numpy as np
from .consts import TextureSuffixes

def import_pillow():
    try:
        from PIL import Image, ImageOps
        return  Image, ImageOps
    except ImportError:
        from . import module_install
        module_install.ensure_pillow_installed()
        from PIL import Image, ImageOps
        return  Image, ImageOps

def set_alpha_to_0(path):
        Image, ImageOps = import_pillow()
        img = Image.open(path).convert("RGBA")
        img.putalpha(0)
        img.save(path)


def _correct_bit_depth(image):
    img = image
    Image, ImageOps = import_pillow()

    arr = np.array(img)

    if arr.ndim == 3:
        if arr.dtype == np.uint16:
            r, g, b = arr[..., 0].astype(np.uint32), arr[..., 1].astype(np.uint32), arr[..., 2].astype(np.uint32)
            gray16 = (0.299*r + 0.587*g + 0.114*b).astype(np.uint16)
            arr_gray = gray16
        else:
            r, g, b = arr[..., 0].astype(np.float32), arr[..., 1].astype(np.float32), arr[..., 2].astype(np.float32)
            gray8 = (0.299*r + 0.587*g + 0.114*b).round().astype(np.uint8)
            arr_gray = gray8
    else:
        arr_gray = arr

    if arr_gray.dtype == np.uint16:
        arr8 = (arr_gray >> 8).astype(np.uint8)
    elif arr_gray.dtype == np.int32 or arr_gray.dtype == np.int64 or arr_gray.dtype == np.float32 or arr_gray.dtype == np.float64:
        mn, mx = float(arr_gray.min()), float(arr_gray.max())
        if mx == mn:
            arr8 = np.zeros(arr_gray.shape, dtype=np.uint8)
        else:
            arr8 = (255.0 * (arr_gray - mn) / (mx - mn)).round().astype(np.uint8)
    else:
        arr8 = arr_gray.astype(np.uint8)

    pil = Image.fromarray(arr8, mode="L")
    return pil

def combine_maos(mtz, mtz_path):
        Image, ImageOps = import_pillow()
        img = Image

        default_size = (512, 512)
        textures = [mtz.metallic_texture, mtz.ao_texture, mtz.smoothness_texture]
        for tex in textures:
             if(tex):
                    tex_path = tex.filepath_from_user()
                    tex_img = Image.open(tex_path)
                    default_size = tex_img.size


        if(mtz.metallic_texture):
            metallic_path = mtz.metallic_texture.filepath_from_user()
            metallic = Image.open(metallic_path)
            metallic = _correct_bit_depth(metallic)
        else:
            metallic = Image.new("L", default_size, 0)

        if(mtz.ao_texture):
            ao_path = mtz.ao_texture.filepath_from_user()
            ao = Image.open(ao_path)
            ao = _correct_bit_depth(ao)

            default_size = ao.size
        else:
            ao = Image.new("L", default_size, 255)
            
        if(mtz.smoothness_texture):
            smoothness_path = mtz.smoothness_texture.filepath_from_user()
            smoothness = Image.open(smoothness_path)
            smoothness = _correct_bit_depth(smoothness)
            if(not mtz.is_smoothness):
                smoothness = ImageOps.invert(smoothness)

            default_size = smoothness.size
        else:
            smoothness = Image.new("L", default_size, 255)

        b_img = Image.new("L", default_size, 0)

        rgba = Image.merge("RGBA", (metallic, ao, b_img, smoothness))

        filename = "%s tex %s%s" % (mtz.name, TextureSuffixes.MAOS, ".png")
        output_path = os.path.join(mtz_path, filename)
        rgba.save(output_path)


def invert_normal_map(image_path):
        Image, ImageOps = import_pillow()
        img = Image.open(image_path).convert("RGBA")
        
        r, g, b, a = img.split()
        
        inverted_g = ImageOps.invert(g)
        
        modified_img = Image.merge("RGBA", (r, inverted_g, b, a))
        
        modified_img.save(image_path)