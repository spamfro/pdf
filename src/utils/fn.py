from functools import reduce, partial
from itertools import groupby


pipe = lambda *fns: reduce(lambda acc, fn: lambda x: fn(acc(x)), fns)
compose = lambda *fns: pipe(*reversed(fns))
branch = lambda *fns: lambda x: (fn(x) for fn in fns)
converge = lambda fn0, fns: pipe(
  lambda x: (fn(x) for fn in fns), 
  lambda xs: fn0(*xs)
)

imap = lambda fn: partial(map, fn)
ifilter = lambda fn: partial(filter, fn)

pick = lambda field: lambda obj: obj[field]

lens_view = lambda lens, store: lens.view(store)
lens_set = lambda lens, value, store: lens.set(value, store)
lens_over = lambda lens, fn, store: lens_set(lens, fn(lens_view(lens, store)), store)

class group_value_lens:
  @staticmethod
  def view(group): return group[1]
  @staticmethod
  def set(value, group): return (group[0], value)

over_group_value = lambda fn: partial(lens_over, group_value_lens, fn)

sort_by = lambda fn: partial(sorted, key=fn)
group_by = lambda fn: partial(groupby, key=fn)

join_str = lambda delim: delim.join
