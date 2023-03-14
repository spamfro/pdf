from collections import namedtuple
from functools import reduce, partial
from itertools import groupby
from pdfplumber import open
from pdfplumber.page import Page
from re import compile
from utils.fn import pipe, pick, map_groups
from utils.json import dump_json


label = namedtuple('label', ['top', 'left', 'text'])
label_top = lambda label: label.top
label_left = lambda label: label.left
label_text = lambda label: label.text

word_to_label = lambda word: label(int(word['top']), int(word['x0']), word['text'])
transform_words_to_labels = partial(map, word_to_label)

# select_significant_words = partial(filter, lambda label: label.left > 20)

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
  partial(Page.extract_words, keep_blank_chars=True, y_tolerance=0),
  transform_words_to_labels,
  # select_significant_words,
  group_by_label_top,
  sort_by_label_left,
  transform_labels_to_text,
  partial(map, partial(pick, 1)),
  list,
  dump_json
)

def digest_pdf(file_path):
  with open(file_path) as pdf:
    return digest_page(pdf.pages[0])
