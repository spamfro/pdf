from sofiyskavoda.parse import parse_digest
from sys import stderr
from utils.json import dump_json
from utils.parse import valid_or_error_data
from utils.pdf import digest_pdf
import argparse

def main(file_path):
  data = valid_or_error_data(parse_digest(digest_pdf(file_path)))
  if 'error' in data: print(dump_json((file_path, data)), file=stderr)
  else: print(dump_json(data))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    args = parser.parse_args()
    main(**vars(args))
