import datetime
import json

class IterEncoder(json.JSONEncoder):
    """
    JSON Encoder that encodes iterators as well.
    Write directly to file to use minimal memory
    """

    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        if isinstance(o, datetime.datetime):
            return str(o)
            
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)

def dump_json(o):
    return json.dumps(o, cls=IterEncoder, ensure_ascii=False).encode('utf-8').decode()
