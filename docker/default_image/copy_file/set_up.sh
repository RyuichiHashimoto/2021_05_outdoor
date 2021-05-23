#!/bin/bash

#### update package tool
apt update
apt -y upgrade
apt-get update
apt-get -y upgrade


#### install 
apt-get install xz-utils liblzma-dev
apt install -y libssl-dev
apt-get install -y libffi-dev
apt install openssl
apt-get install -y wget build-essential unzip
apt-get install -y zlib1g-dev
apt-get install -y libbz2-dev
apt-get install -y vim

#### install python3
cd /root
wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tar.xz
tar Jxfv Python-3.7.9.tar.xz
cd Python-3.7.9
./configure
make altinstall


###  reflect the bash setting file
source ~/.bashrc

#### install python module
cd /root
pip3.7 install -r requirement.txt
pip3.7 install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

#### janestreet
cd /root/
unzip data.zip
cd /root/data/

cp -r janestreet /usr/local/lib/python3.7/site-packages
cp *.* /usr/local/lib/python3.7/site-packages
