"""
PYTHONPATH+=./src python3 ./src/parse_sofiyskavoda_pdf.py ./data/__confidential/sofiyskavoda.pdf
find ./data/__confidential/sofiyskavoda -name '*.pdf' | PYTHONPATH+=./src xargs -L1 python3 ./src/parse_sofiyskavoda_pdf.py | grep error
"""

from sofiyskavoda.parse import parse_digest
from utils.json import dump_json
from utils.pdf import digest_pdf
import argparse

def main(file_path):
  print(dump_json(parse_digest(digest_pdf(file_path))))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    args = parser.parse_args()
    main(**vars(args))
