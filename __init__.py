bl_info = {
	"name": "HF2 Materializer Creator",
	"description": "Tool for creating HF2 Materializer mods",
	"author": "brushie",
	"version": (0, 8, 5),
	"blender": (4, 0, 0),
	"location": "3D View > Toolbox",
	"category": "Object",
}

modules_names = ['props','ui','preferences', 'core_operators','utils', 'materializer_loader', 'module_install']

modules_full_names = {}
for current_module_name in modules_names:
	modules_full_names[current_module_name] = ('{}.{}'.format(__name__, current_module_name))

import sys
import importlib


for current_module_full_name in modules_full_names.values():
	if current_module_full_name in sys.modules:
		importlib.reload(sys.modules[current_module_full_name])
	else:
		globals()[current_module_full_name] = importlib.import_module(current_module_full_name)
		setattr(globals()[current_module_full_name], 'modulesNames', modules_full_names)

def register():
	for current_module_name in modules_full_names.values():
		if current_module_name in sys.modules:
			if hasattr(sys.modules[current_module_name], 'register'):
				sys.modules[current_module_name].register()

def unregister():
	for current_module_name in modules_full_names.values():
		if current_module_name in sys.modules:
			if hasattr(sys.modules[current_module_name], 'unregister'):
				sys.modules[current_module_name].unregister()