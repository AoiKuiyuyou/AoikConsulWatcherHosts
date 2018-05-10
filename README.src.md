[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
# AoikConsulWatcherHosts
Watch changes of Consul services and update hosts file.

Tested woring with:
- Python 3.6.5, 2.7.14

## Table of Contents
[:toc(beg='next', indent=-1)]

## Setup
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikConsulWatcherHosts

cd AoikConsulWatcherHosts

pip install -r aoikconsulwatcher/requirements.txt
```

## Usage
[:tod()]

### Edit config module
Edit AoikConsulWatcher config module [aoikconsulwatcher/conf/config.py](/aoikconsulwatcher/conf/config.py). This config module specifies the Consul
server to connect to, and the handler `handle_service_infos` to be called on changes of Consul services. The handler updates hosts file.

### Run program
Run:
```
cp /etc/hosts /etc/hosts.backup

cd AoikConsulWatcherHosts

export CONSUL_HOST=127.0.0.1
export CONSUL_PORT=8500
export DOMAIN_IP=127.0.0.1

python aoikconsulwatcher/src/aoikconsulwatcher/__main__.py --config aoikconsulwatcher/conf/config.py
```

## Docker
[:tod()]

### Run image
Run:
```
cp /etc/hosts /etc/hosts.backup

docker run -it \
    -v /etc/hosts:/etc/hosts \
    -e CONSUL_HOST=127.0.0.1 \
    -e CONSUL_PORT=8500 \
    -e DOMAIN_IP=127.0.0.1 \
    aoikuiyuyou/aoikconsulwatcherhosts
```
Or:
```
cp /etc/hosts /etc/hosts.backup

cd AoikConsulWatcherHosts

docker-compose -f docker/docker-compose.yml up
```

To use a custom AoikConsulWatcher config module e.g. `/config.py`, run:
```
cp /etc/hosts /etc/hosts.backup

docker run -it \
    -v /config.py:/opt/aoikconsulwatcherhosts/aoikconsulwatcher/conf/config.py \
    -v /etc/hosts:/etc/hosts \
    -e CONSUL_HOST=127.0.0.1 \
    -e CONSUL_PORT=8500 \
    -e DOMAIN_IP=127.0.0.1 \
    aoikuiyuyou/aoikconsulwatcherhosts
```

### Build image
Run:
```
cd AoikConsulWatcherHosts

docker build -t aoikuiyuyou/aoikconsulwatcherhosts -f docker/Dockerfile .
```
