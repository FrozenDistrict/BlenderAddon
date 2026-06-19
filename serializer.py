from json import JSONEncoder

import json

from . import data_exporter



def Serialize(o):
    jsonString = Hf2ItemEncoder().encode(o)
    print(jsonString)
    return jsonString

class Hf2ItemEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, data_exporter.MaterializerContainer):
            uv_units = []
            for i in o.uv_unit_sizes:
                uv_units.append(float(i.name))
                uv_units = sorted(uv_units)
            o.__dict__['uv_unit_sizes'] = uv_units
            

            return  o.__dict__