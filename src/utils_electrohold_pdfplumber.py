from functools import reduce, partial
from pdfplumber import open


"""
open :: pdfplumber ~> file_path -> pdf

pages :: pdf ~> [page]

crop ``:: page ~> bbox -> page
filter :: page ~> fn -> page
objects :: page ~> { object_type -> object }
"""

pipe = lambda *fns: reduce(lambda acc, fn: lambda x: fn(acc(x)), fns)
map_groups = lambda fn, groups: map(lambda group: (group[0], fn(group[1])), groups)

page_objects = lambda page: page.objects.items()

page_to_lines = pipe(
  page_objects,
  # pipe(partial(map_groups, len), list)
  partial(filter, lambda it: it[0] in ['line', 'rect']),
  list
)
  
def index_pdf(file_path):
  with open(file_path) as pdf:
    return page_to_lines(pdf.pages[0])


# def index_page(page):
#   print('objects', type(page.objects), len(page.objects), page.objects.keys(), list(page.objects))
#   print('chars', type(page.chars), len(page.chars))
#   print('lines', type(page.lines), len(page.lines))
#   print('rects', type(page.rects), len(page.rects))
#   print('curves', type(page.curves), len(page.curves))
#   print('images', type(page.images), len(page.images))
#   print('annots', type(page.annots), len(page.annots))
    