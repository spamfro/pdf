"""
digest_pdf :: file_path -> [str]
"""

from functools import partial
from operator import add
from pdfplumber import open as open_pdf
from pdfplumber.page import Page
from re import compile
from utils.fn import ifilter, group_by, group_value_lens, imap, ireduce, join_str, pick, pipe, sort_by, strip_str
from utils.ranges import number_in_number_ranges


mul = lambda x: lambda y: x * y
pts_to_mm = mul(1/72 * 2.54 * 10)

number_with_spaces_pattern = compile(r'[\s\d,]+')
normalize_number = lambda text: text.replace(' ', '') if number_with_spaces_pattern.fullmatch(text) else text

extract_page_words = partial(Page.extract_words, keep_blank_chars=True, y_tolerance=0, x_tolerance=1)

word_dimention = lambda key: pipe(pick(key), pts_to_mm)
word_top = word_dimention('top')
word_left = word_dimention('x0')
word_right = word_dimention('x1')
word_top_left = lambda word: (word_top(word), word_left(word))
word_text = pipe(pick('text'), strip_str(), normalize_number)

sort_words_by_word_top_left = sort_by(word_top_left)
group_words_in_lines_by_word_top = pipe(group_by(word_top), imap(group_value_lens.view))

def group_words_next_to_each_other(words, distance=1):
  rs = []
  prev_word = None
  for word in words:
    if prev_word is None or word_left(word) - word_right(prev_word) > distance:
      rs.append([word])
    else:
      rs[-1].append(word)
    prev_word = word
  return rs

collate_words_text = pipe(imap(word_text), join_str(' '))
line_words_to_text = pipe(
  group_words_next_to_each_other,
  imap(collate_words_text), 
  join_str(' ___ ')
)
transform_lines_words_to_text = imap(line_words_to_text)

digest_page = pipe(
  extract_page_words,
  sort_words_by_word_top_left,
  group_words_in_lines_by_word_top,
  transform_lines_words_to_text,
  list
)

digest_pdf_pages = pipe(imap(digest_page), ireduce(add))

page_number = lambda page: page.page_number
is_page_in_pages_ranges = lambda pages_ranges: (
  pipe(page_number, partial(number_in_number_ranges, pages_ranges)) if pages_ranges
  else lambda _: True
)
digest_pdf_pages_ranges = lambda pages_ranges: (
  pipe(ifilter(is_page_in_pages_ranges(pages_ranges)), digest_pdf_pages)
)

def digest_pdf(file_path, pages_ranges):
  with open_pdf(file_path) as pdf:
    return digest_pdf_pages_ranges(pages_ranges)(pdf.pages)
