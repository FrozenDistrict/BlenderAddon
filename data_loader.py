import bpy
from bpy.props import EnumProperty, StringProperty
from pathlib import Path


_TAG_ENUM_ITEMS = []
_TAGS_LOADED_FROM = None



def _tags_path(type):
    if type == "item_kind":
        return Path(__file__).resolve().parent / "hf_data/ItemKind.tags"

    if type == "item_category":
        return Path(__file__).resolve().parent / "hf_data/ItemCategory.tags"

    if type == "item_tag":
        return Path(__file__).resolve().parent / "hf_data/ItemTag.tags"

    if type == "item_series":
        return Path(__file__).resolve().parent / "hf_data/ItemSeries.tags"



def _parse_tags_file(filepath: str):
    filepath = str(filepath)
    result = []
    stack = [] 

    with open(filepath, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\r\n")

            if not line.strip():
                continue

            stripped = line.lstrip("\t ")
            indent_part = line[:len(line) - len(stripped)]

            level = indent_part.count("\t") + (indent_part.count(" ") // 4)

            name = stripped.strip()

            stack = stack[:level]
            stack.append(name)

            result.append("/".join(stack))

    return result


def _load_tags_as_enum_items(filepath: str):
    items = []
    for full_path in _parse_tags_file(filepath):
        identifier = full_path
        name = full_path.replace("/", " / ")
        description = f"Tag: {name}"
        items.append((identifier, name, description))

    return items



def _filter_tags_by_prefix(tags, prefix):
    return [tag for tag in tags if tag[0].startswith(prefix)]

def _filter_tags_by_root(tags, root):
    return [tag for tag in tags if tag[0] == root or tag[0].startswith(root + "/")]

def _add_none(tags):
    none_item = ("", "None", "No tag")
    return [none_item] + tags

def _number_items(tags):
    return [(identifier, name, description, i) for i, (identifier, name, description) in enumerate(tags)]


def load_tags(type, filter_prefix = None, filter_root = None):
    tags = _load_tags_as_enum_items(_tags_path(type))

    if filter_prefix is not None:
        tags = _filter_tags_by_prefix(tags, filter_prefix)

    if filter_root is not None:
        tags = _filter_tags_by_root(tags, filter_root)

    return _number_items(_add_none(tags))













