import argparse

from utils_json import dump_json
from utils_electrohold_pdfminersix import index_pdf


def main(file_path):
  # print(dump_json(index_pdf(file_path)))
  print(index_pdf(file_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    args = parser.parse_args()
    main(**vars(args))
