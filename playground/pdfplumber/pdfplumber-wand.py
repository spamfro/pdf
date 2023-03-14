import argparse
import pdfplumber


def main(file_path):
  pdf = pdfplumber.open(file_path)
  pdf.pages[0].to_image()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('file_path', type=str, help='file path')
  args = parser.parse_args()
  main(**vars(args))
