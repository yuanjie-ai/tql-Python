#!/usr/bin/env bash
apt-get update;
export DEBIAN_FRONTEND=noninteractive;
apt-get install -y tzdata;
ln -fs /usr/share/zoneinfo/PRC /etc/localtime;
dpkg-reconfigure --frontend noninteractive tzdata;