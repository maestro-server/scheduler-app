
import json

def transformParams(args, objs):

    for key, val in objs.items():

        if isinstance(val, (list, dict, tuple, set)):
            val = json.dumps(val)

        args.append({
            'key': key,
            'value': val
        })

    return objs