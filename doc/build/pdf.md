# Read PDF

### Run Python container
```
docker container run --rm -it -d \
  --name dev-python \
  --network bridge-dev \
  --ip 172.20.0.100 \
  --volume "$PWD:/home/george/ws" \
  --publish 8888:8888 \
  dev-python

docker container attach --detach-keys="ctrl-x" dev-python
```

### Build and run
```
cd ~/ws
pip3 install -r src/requirements.txt
python3 src/read-pdf-pdfminersix.py secrets/electrohold.pdf
python3 src/read-pdf-pdfplumber.py secrets/electrohold.pdf
python3 src/read-pdf-pypdf.py secrets/electrohold.pdf
```
