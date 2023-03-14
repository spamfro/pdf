from collections import namedtuple
from functools import partial
from itertools import groupby
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal
from re import compile
from utils.fn import pipe, pick, map_groups
from utils.json import dump_json


def flatten_text_elements(elements):
  queue = [elements]
  while len(queue) > 0:
    element = next(queue[0], None)
    if element is None: queue.pop(0)
    elif isinstance(element, LTTextLineHorizontal): yield element
    elif isinstance(element, LTTextBoxHorizontal): queue.insert(0, iter(element))

label = namedtuple('label', ['top', 'left', 'text'])
label_top = lambda label: label.top
label_left = lambda label: label.left
label_text = lambda label: label.text

element_to_label = lambda element: label(-int(element.y0), int(element.x0), element.get_text().strip(' \n'))
transform_elements_to_labels = partial(map, element_to_label)

select_significant_labels = partial(filter, lambda label: label.left > 20)

group_by_label_top = pipe(partial(sorted, key=label_top), partial(groupby, key=label_top))
sort_by_label_left = partial(map_groups, partial(sorted, key=label_left))

number_with_spaces_pattern = compile(r'[\s\d,]+')
normalize_number = lambda text: text.replace(' ', '') if number_with_spaces_pattern.fullmatch(text) else text

labels_to_text = pipe(
  partial(map, label_text), 
  partial(map, normalize_number),
  partial(' '.join)
)

transform_labels_to_text = partial(map_groups, labels_to_text)

digest_page = pipe(
  iter,
  flatten_text_elements,
  transform_elements_to_labels,
  select_significant_labels,
  group_by_label_top,
  sort_by_label_left,
  transform_labels_to_text,
  partial(map, partial(pick, 1)),
  list,
  dump_json,
)

digest_pdf = pipe(
  extract_pages,
  next,
  digest_page
)
