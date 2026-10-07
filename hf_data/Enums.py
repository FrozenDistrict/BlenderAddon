avaliability = [
    ('0', "FreelyAvailable", "Use materializer for Flipper and Architect"),
    ('1', "RequireArchitect", "Use materializer only for Architect"),
]

mtz_type = [
    ('0', "Materializer", ""),
    ('1', "Pattern", "")
]

allowed_rotations = [
    ('0', "None", ""),
    ('1', "Snap 45 Max 180 - 0, 45, 90, 135 ", ""),
    ('2', "Snap 90 Max 180 - 0, 90", ""),
    ('3', "Snap 45 Max 360 - 0, 45, 90, 135, 180, 225, 270, 315", ""),
    ('4', "Snap 90 Max 360 - 0, 90, 180, 270", ""),
]

pattern_usage = [
    ('0', "Walls and Items", ""),
    ('1', "Items", ""),
    ('2', "Walls", ""),
]

item_kind = [
    ("", "None", "No item kind", 0),
    ("Wood panels", "Wood panels", "", 1),
    ("Wallpaper", "Wallpaper", "", 2),
    ("Paint", "Paint", "", 3),
    ("Stone", "Stone", "", 4),
    ("Metal panels/tiles", "Metal panels/tiles", "", 5),
    ("Carpets", "Carpets", "", 6),
    ("Damaged materials", "Damaged materials", "", 7),
    ("Other", "Other", "", 8),
]

item_kind_export = {
    "Wood panels" : "Oak panels",
    "Wallpaper" : "Floral wallpaper",
    "Paint" : "Black paint",
    "Stone" : "White marble tiles",
    "Metal panels/tiles" : "Copper tiles",
    "Carpets" : "Poplin carpet tiles",
    "Damaged materials" : "Damaged materials",
    "Other" : "Other",
}

def export_item_kind(item_kind_value):
    item_kind_value = item_kind_value.strip()
    return item_kind_export.get(item_kind_value, item_kind_value)

avaliability_export = {
    "0" : "FreelyAvailable",
    "1" : "RequireArchitect"
}

allowed_rotations_export = {
    "0" : "None",
    "1" : "Snap45Max180",
    "2" : "Snap90Max180",
    "3" : "Snap45Max360",
    "4" : "Snap90Max360",
}

mtz_type_export = {
    "0" : "Materializer",
    "1" : "Pattern"
}
pattern_usage_export = {
    "0" : "WallsAndItems",
    "1" : "Items",
    "2" : "Walls",
}
