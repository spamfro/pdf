import argparse
import ezodf
from itertools import tee, islice

def main(file_path, sheet_name):
  sheet_name = sheet_name or 'hist'

  doc = ezodf.opendoc(file_path)
  table = doc.sheets[sheet_name]
  table_rows = table.rows()
  header_row = list(next(table_rows))

  row_values = lambda row: list(cell.value for cell in row)

  print(row_values(header_row))
  print(list(map(row_values, islice(table_rows, 10))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    parser.add_argument('--sheet-name', type=str, help='sheet name')
    args = parser.parse_args()
    main(**vars(args))
