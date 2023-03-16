"""
digest_pdf :: file_path -> [str]
"""

from functools import partial
from operator import add
from pdfplumber import open
from pdfplumber.page import Page
from pdfplumber.pdf import PDF
from re import compile
from utils.fn import group_value_lens, pipe, group_by, imap, ireduce, join_str, over_group_value, sort_by

extract_words = partial(Page.extract_words, keep_blank_chars=True, y_tolerance=0)

word_line_top = lambda word: int(word['top'])
word_pos_left = lambda word: int(word['x0'])
word_text = lambda word: word['text'].strip(' \n')

group_words_by_line_top = pipe(sort_by(word_line_top), group_by(word_line_top))

sort_group_words_by_pos_left = imap(over_group_value(sort_by(word_pos_left)))

number_with_spaces_pattern = compile(r'[\s\d,]+')
normalize_number = lambda text: text.replace(' ', '') if number_with_spaces_pattern.fullmatch(text) else text
transform_word_to_text = pipe(word_text, normalize_number)
transform_words_to_text = pipe(imap(transform_word_to_text), join_str(' '))
transform_group_to_text = pipe(over_group_value(transform_words_to_text), group_value_lens.view)
transform_group_words_to_text = imap(transform_group_to_text)

digest_page = pipe(
  extract_words,
  group_words_by_line_top,
  sort_group_words_by_pos_left,
  transform_group_words_to_text,
  list
)

digest_pdf_pages = pipe(imap(digest_page), ireduce(add), list)

def digest_pdf(file_path):
  with open(file_path) as pdf:
    return digest_pdf_pages(pdf.pages)
