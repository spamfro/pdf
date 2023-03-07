import argparse

from pdfminer.high_level import extract_text


def main(file_path):
  text = extract_text(file_path)

  print(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    args = parser.parse_args()
    main(**vars(args))
