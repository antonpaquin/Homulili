from copy import deepcopy
import json


def printer(input):
    inp = input.get()

    if hasattr(inp, '__dict__'):
        try:
            d = deepcopy(inp.__dict__)
            d = {key: value for key, value in d.items() if not key[0:2] == '__'}
            print(json.dumps(d, indent=4))
        except Exception:
            pass

    if isinstance(inp, str):
        print(inp)

    print(inp)
