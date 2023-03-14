from functools import reduce

pipe = lambda *fns: reduce(lambda acc, fn: lambda x: fn(acc(x)), fns)
compose = lambda *fns: pipe(*reversed(fns))
branch = lambda *fns: lambda x: (fn(x) for fn in fns)
converge = lambda fn0, fns: pipe(
    lambda x: (fn(x) for fn in fns), 
    lambda xs: fn0(*xs)
)

pick = lambda field, obj: obj[field]
map_groups = lambda fn, groups: map(lambda group: (group[0], fn(group[1])), groups)
