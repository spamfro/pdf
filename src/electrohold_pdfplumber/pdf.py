"""
digest_pdf :: file_path -> [str]
"""

from functools import partial
from pdfplumber import open
from pdfplumber.page import Page
from re import compile
from utils.fn import pipe, group_value_lens, imap, ifilter, sort_by, group_by, over_group_value, join_str


extract_words = partial(Page.extract_words, keep_blank_chars=True, y_tolerance=0)

element_line_top = lambda element: int(element['top'])
element_pos_left = lambda element: int(element['x0'])
element_text = lambda element: element['text'].strip(' \n')

group_elements_by_line_top = pipe(sort_by(element_line_top), group_by(element_line_top))

sort_group_elements_by_pos_left = imap(over_group_value(sort_by(element_pos_left)))

number_with_spaces_pattern = compile(r'[\s\d,]+')
normalize_number = lambda text: text.replace(' ', '') if number_with_spaces_pattern.fullmatch(text) else text
transform_element_to_text = pipe(element_text, normalize_number)
transform_elements_to_text = pipe(imap(transform_element_to_text), join_str(' '))
transform_group_to_text = pipe(over_group_value(transform_elements_to_text), group_value_lens.view)
transform_group_elements_to_text = imap(transform_group_to_text)

digest_page = pipe(
  extract_words,
  group_elements_by_line_top,
  sort_group_elements_by_pos_left,
  transform_group_elements_to_text,
  list,
)

def digest_pdf(file_path):
  with open(file_path) as pdf:
    return digest_page(pdf.pages[0])
