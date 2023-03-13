import functools

pipe = lambda *fns: functools.reduce(lambda acc, fn: lambda x: fn(acc(x)), fns)
compose = lambda *fns: pipe(*reversed(fns))
branch = lambda *fns: lambda x: (fn(x) for fn in fns)
converge = lambda fn0, fns: pipe(
    lambda x: (fn(x) for fn in fns), 
    lambda xs: fn0(*xs)
)
