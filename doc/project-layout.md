# Project layout

### Source tree
```
data/
  __confidential/ electrohold.pdf, ...
  
src/
  utils/ json.py, fn.py, ...
  electrohold/ pdf.py, ...
  digest_electrohold.py
```

### Run app
```
PYTHONPATH+=./src python3 src/digest_electrohold.py data/__confidential/electrohold.pdf
```

### App main (./src/digest_electrohold.py)
```python
import argparse
from electrohold.pdf import digest_pdf

def main(file_path):
  print(digest_pdf(file_path))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    args = parser.parse_args()
    main(**vars(args))
```

### App module (./src/electrohold/pdf.py)
```python
from utils.json import dump_json

digest_pdf = ...
```
