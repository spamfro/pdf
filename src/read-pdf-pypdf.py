import argparse
import PyPDF2    # https://pypdf2.readthedocs.io/en/3.0.0/


def main(file_path):
  pdf = PyPDF2.PdfReader(file_path)

  print('pages', type(pdf.pages), len(pdf.pages))
  
  page = pdf.pages[0]
  print('page', type(page), len(page), list(page))

  contents = page.get_contents()
  print('contents', type(contents), len(contents), list(contents))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    args = parser.parse_args()
    main(**vars(args))
