import json
import bpy
import os
import random

from .hf_data import Enums
from . import utils
from . import serializer
from .consts import Defaults

class MaterializerContainer():
    def __init__(self):
        self.name = []
        self.type = []
        self.is_grimy = []
        self.custom_colors = []
        self.availability = []
        self.uv_unit_sizes = []

        self.materializer_stid = []
        self.surfacer_category = []

        self.support_pattern = []
        self.support_mosaic = []

        self.allowed_rotations = []
        self.pattern_usage = []


        self.item_kind = []
        self.item_series = []
        self.affordability = []
        self.shop_category = []
        self.price = []

        self.x_factor = 0
        #self.invert_mask_alpha = []
        
def export_data(mtz, mtz_path):
    mtzContainer = MaterializerContainer()

    mtzContainer.name = mtz.name
    mtzContainer.type = Enums.mtz_type_export[mtz.type]

    mtzContainer.is_grimy = mtz.is_grimy
    mtzContainer.support_pattern = mtz.support_pattern
    mtzContainer.support_mosaic = mtz.support_mosaic

    mtzContainer.allowed_rotations = Enums.allowed_rotations_export[mtz.allowed_rotations]
    mtzContainer.pattern_usage = Enums.pattern_usage_export[mtz.pattern_usage]

    mtzContainer.availability = Enums.avaliability_export[mtz.avaliability]
    mtzContainer.custom_colors = mtz.custom_colors
    mtzContainer.uv_unit_sizes = mtz.uv_unit_sizes

    mtzContainer.materializer_stid = mtz.materializer_stid
    mtzContainer.surfacer_category = mtz.materializer_category.strip()

    #mtzContainer.invert_mask_alpha = mtz.invert_mask_alpha

    article_data = mtz.article_data
    mtzContainer.item_kind = article_data.item_kind.strip()
    mtzContainer.item_series = article_data.item_series.strip()
    mtzContainer.affordability = article_data.affordability.strip()
    mtzContainer.shop_category = article_data.shop_category.strip()
    mtzContainer.price = article_data.price

    if mtzContainer.affordability:
        mtzContainer.x_factor = _ensure_x_factor(article_data)


    data = serializer.serialize(mtzContainer)

    file_name_json = os.path.join(mtz_path,"%s data.json" % (mtz.name))

    save_JSON_file(file_name_json, data)

def _ensure_x_factor(article_data):
    if article_data.x_factor == 0:
        article_data.x_factor = random.randint(20, 100)
    return article_data.x_factor

def save_JSON_file(file_name_json, data):
    print(f"Saving {file_name_json}")
    with open(file_name_json, "w") as f:
        f.write(data)









