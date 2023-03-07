import argparse
import pdfplumber   # https://pypi.org/project/pdfplumber/

from itertools import islice 


def main(file_path):
  with pdfplumber.open(file_path) as pdf:
    print('pages', type(pdf.pages), len(pdf.pages))
    print()

    page = pdf.pages[0]
    print('objects', type(page.objects), len(page.objects), page.objects.keys(), list(page.objects))
    print('chars', type(page.chars), len(page.chars))
    print('lines', type(page.lines), len(page.lines))
    print('rects', type(page.rects), len(page.rects))
    print('curves', type(page.curves), len(page.curves))
    print('images', type(page.images), len(page.images))
    print('annots', type(page.annots), len(page.annots))
    print()

    line = page.lines[0]
    print('line.keys', list(line))
    print('line', line)
    print()

    char = page.chars[0]
    print('char.keys', list(char))
    print('char', char)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    args = parser.parse_args()
    main(**vars(args))
