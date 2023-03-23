# Digest PDF with Python

## Run 
```
pip3 install -r requirements.txt
PYTHONPATH+=./src python3 src/digest_pdf.py data/__confidential/electrohold.pdf
PYTHONPATH+=./src python3 src/digest_pdf.py data/__confidential/toplofikaciya.pdf --pages 1,2
PYTHONPATH+=./src python3 src/digest_pdf.py data/__confidential/sofiyskavoda.pdf --pages 1-2
```

## Setup Python environment with Docker

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
    useradd -m -s /bin/bash -G sudo george && \
    cat /run/secrets/PASSWD | chpasswd
EOF
```

### Create docker Python image
```
docker image build --no-cache --force-rm --tag dev-python - << EOF
  FROM dev-ubuntu
  RUN apt-get update && apt-get install -y tmux vim curl less python3 python3-pip libmagickwand-dev
  USER george
  ENV PATH "$PATH:/home/george/.local/bin"
  RUN pip3 install notebook Wand
EOF
```

### Run Python container
```
docker container run --rm -it -d \
  --name dev-python \
  --network bridge-dev \
  --ip 172.20.0.100 \
  --volume "$PWD:$PWD" \
  --publish 8888:8888 \
  dev-python

docker container attach --detach-keys="ctrl-x" dev-python
docker container exec -it --user george dev-python /bin/bash

docker container stop dev-python
```

### Run jupyter notebook
```
docker container exec -it --user george dev-python jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser
```

### Update Wand policy to read PDF
```
vim /etc/ImageMagick-6/policy.xml
  <policy domain="coder" rights="read" pattern="PDF" />
```
