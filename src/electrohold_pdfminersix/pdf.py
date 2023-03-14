"""
digest_pdf :: file_path -> [str]
"""

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal
from re import compile
from utils.fn import pipe, group_value_lens, imap, ifilter, sort_by, group_by, over_group_value, join_str


def flatten_text_elements(elements):
  queue = [elements]
  while len(queue) > 0:
    element = next(queue[0], None)
    if element is None: queue.pop(0)
    elif isinstance(element, LTTextLineHorizontal): yield element
    elif isinstance(element, LTTextBoxHorizontal): queue.insert(0, iter(element))

element_line_top = lambda element: -int(element.y0)
element_pos_left = lambda element: int(element.x0)
element_text = lambda element: element.get_text().strip(' \n')

is_significant_element = lambda element: element.x0 > 50
select_significant_elements = ifilter(is_significant_element)

group_elements_by_line_top = pipe(sort_by(element_line_top), group_by(element_line_top))

sort_group_elements_by_pos_left = imap(over_group_value(sort_by(element_pos_left)))

number_with_spaces_pattern = compile(r'[\s\d,]+')
normalize_number = lambda text: text.replace(' ', '') if number_with_spaces_pattern.fullmatch(text) else text
transform_element_to_text = pipe(element_text, normalize_number)
transform_elements_to_text = pipe(imap(transform_element_to_text), join_str(' '))
transform_group_to_text = pipe(over_group_value(transform_elements_to_text), group_value_lens.view)
transform_group_elements_to_text = imap(transform_group_to_text)

digest_page = pipe(
  iter,
  flatten_text_elements,
  select_significant_elements,
  group_elements_by_line_top,
  sort_group_elements_by_pos_left,
  transform_group_elements_to_text,
  list,
)

digest_pdf = pipe(
  extract_pages,
  next,
  digest_page
)
