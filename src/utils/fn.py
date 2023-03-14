from functools import reduce, partial
from collections import namedtuple

pipe = lambda *fns: reduce(lambda acc, fn: lambda x: fn(acc(x)), fns)
compose = lambda *fns: pipe(*reversed(fns))
branch = lambda *fns: lambda x: (fn(x) for fn in fns)
converge = lambda fn0, fns: pipe(
  lambda x: (fn(x) for fn in fns), 
  lambda xs: fn0(*xs)
)

pick = lambda field, obj: obj[field]


lens_view = lambda lens, store: lens.view(store)
lens_set = lambda lens, value, store: lens.set(value, store)
lens_over = lambda lens, fn, store: lens_set(lens, fn(lens_view(lens, store)), store)


# map_groups = lambda fn, groups: map(lambda group: (group[0], fn(group[1])), groups)
# map_groups = lambda fn, groups: ((key, fn(value)) for key, value in groups)

class group_value_lens:
  @staticmethod
  def view(group): return group[1]
  @staticmethod
  def set(value, group): return (group[0], value)

map_groups = lambda fn, groups: map(partial(lens_over, group_value_lens, fn), groups)
