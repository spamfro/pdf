"""
ifilter :: (a -> bool) -> [a] -> [a]
imap :: (a -> b) -> [a] -> [b]
join_str :: str -> [str] -> str
order_by :: (x -> k) -> x... -> [(k,x)]
pick :: str -> obj -> a
pipe :: (fn,...) -> fn
sort_by :: (x -> k) -> x... -> [x]
over_group_value :: (a -> b) -> (k,a) -> (k,b)
"""

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
ireduce = lambda fn: partial(reduce, fn)
izip = lambda *xss: partial(zip, *xss)

id = lambda x: x

pick = lambda k: lambda x: x[k]
picks = lambda *ks: reduce(lambda fn, k: lambda x: fn(x)[k], ks, id) 
ipick = lambda *xs: branch(*(picks(*x.split('.')) for x in xs))

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
strip_str = lambda chars = None: lambda xs: xs.strip(chars)
