# Read ODS

Use [Exodf](https://pythonhosted.org/ezodf/) to load ODS file with Python.

## Setup environment

### Create docker network
```
docker network create \
  -d bridge \
  --subnet 172.20.0.0/16 \
  --gateway 172.20.0.1 \
  bridge-dev
```

### Create docker dev image
```
DOCKER_BUILDKIT=1 \
PASSWD=$(read -s -p 'Password:' PASSWD ; echo "george:$PASSWD") \
docker image build \
  --no-cache \
  --secret id=PASSWD \
  --tag dev-ubuntu \
  - << EOF

  FROM ubuntu
  RUN --mount=type=secret,id=PASSWD \
    apt-get update && \
    apt-get install -y sudo && \
    useradd -m -G sudo george && \
    cat /run/secrets/PASSWD | chpasswd
EOF
```

### Create docker Python image
```
docker image build --tag dev-python - << EOF
  FROM dev-ubuntu
  RUN apt-get update && \
      apt-get install -y tmux vim curl python3 python3-pip
  USER george
  SHELL ["/bin/bash"]
EOF
```

### Run Python container
```
docker container run --rm -it -d \
  --name dev-python \
  --network bridge-dev \
  --ip 172.20.0.100 \
  --volume "$PWD:/home/george/ws" \
  dev-python

docker container attach --detach-keys="ctrl-x" dev-python

docker container stop dev-python
```

## Build and run
```
cd ~/ws

pip3 install -r read-ods/requirements.txt

python3 read-ods/bookkeeping-hist.py secrets/bookkeeping-hist.ods
```


