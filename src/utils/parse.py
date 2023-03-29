from re import compile as compile_regex
import datetime

parse_regex = lambda regex: compile_regex(regex).search

date_from_match = lambda match: datetime.date(int(match.group(3)), int(match.group(2)), int(match.group(1))) if match else None
number_from_match = lambda match: int(match.group(1)) if match else None
float_number_from_match = lambda match: float(match.group(1)) if match else None
  
parse_field = lambda k, fn: lambda x: [(k, r)] if (r := fn(x)) is not None else []
init_data = lambda ks: { k: None for k in ks }
valid_data = lambda data: data if all(value is not None for _, value in data.items()) else None
missing_data = lambda data: [key for key,value in data.items() if value is None]
valid_or_error_data = lambda data: data if len(error := missing_data(data)) == 0 else { 'error': error }

class once():
  def __init__(self, fn):
    self.fn = fn
  def __call__(self, x):
    r = self.fn(x) if self.fn else []
    if len(r) > 0: self.fn = None
    return r
