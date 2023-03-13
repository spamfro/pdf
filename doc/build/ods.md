# Read ODS

Use [Exodf](https://pythonhosted.org/ezodf/) to load ODS file with Python.

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
pip3 install -r read-ods/requirements.txt
python3 read-ods/bookkeeping-hist.py secrets/bookkeeping-hist.ods
```
