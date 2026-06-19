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
    ('3', "Snap 45 Max 360 - 0, 45, 90, 135, 180, 205, 240, 270, 315", ""),
    ('4', "Snap 90 Max 360 - 0, 90, 180, 270", ""),
]

pattern_usage = [
    ('0', "Walls and Items", ""),
    ('1', "Items", ""),
    ('2', "Walls", ""),
]

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
