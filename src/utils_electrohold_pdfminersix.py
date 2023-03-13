from collections import namedtuple
from functools import reduce, partial
from itertools import groupby
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal


pipe = lambda *fns: reduce(lambda acc, fn: lambda x: fn(acc(x)), fns)
sort_by = lambda fn, xs: sorted(xs, key=fn)
group_by = lambda fn, xs: groupby(sorted(xs, key=fn), key=fn)
map_groups = lambda fn, groups: map(lambda group: (group[0], fn(group[1])), groups)


def flatten_text_elements(elements):
  queue = [elements]
  while len(queue) > 0:
    element = next(queue[0], None)
    if element is None: queue.pop(0)
    elif isinstance(element, LTTextLineHorizontal): yield element
    elif isinstance(element, LTTextBoxHorizontal): queue.insert(0, iter(element))

# elements_of_element = lambda element: iter(element) 
label = namedtuple('label', ['top', 'left', 'text'])
label_top = lambda label: label.top
label_left = lambda label: label.left
label_text = lambda label: label.text
label_from_element = lambda element: label(-int(element.y0), int(element.x0), element.get_text().strip(' \n'))
labels_from_elements = partial(map, label_from_element)
select_significant_labels = partial(filter, lambda label: label.left > 50)
group_by_label_top = partial(group_by, label_top)
sort_by_label_left = partial(map_groups, partial(sort_by, label_left))
labels_to_text = partial(map_groups, pipe(partial(map, label_text), list))

lines_from_page = pipe(
  iter,
  flatten_text_elements,
  labels_from_elements,
  select_significant_labels,
  group_by_label_top,
  sort_by_label_left,
  labels_to_text,
  dict
)

index_pdf = pipe(
  extract_pages,
  next,
  lines_from_page
)
