import pdfplumber


def index_pdf(file_path):
  with pdfplumber.open(file_path) as pdf:
    return pdf


# def index_page(page):
#   print('objects', type(page.objects), len(page.objects), page.objects.keys(), list(page.objects))
#   print('chars', type(page.chars), len(page.chars))
#   print('lines', type(page.lines), len(page.lines))
#   print('rects', type(page.rects), len(page.rects))
#   print('curves', type(page.curves), len(page.curves))
#   print('images', type(page.images), len(page.images))
#   print('annots', type(page.annots), len(page.annots))
    