import argparse
from electrohold_pdfminersix.pdf import digest_pdf
# from electrohold_pdfplumber.pdf import digest_pdf

def main(file_path):
  print(digest_pdf(file_path))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    args = parser.parse_args()
    main(**vars(args))
