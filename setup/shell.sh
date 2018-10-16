#!/usr/bin/env bash

# Install Python3's package manager
apt-get -y install python3-pip

# Use Python3's package manager to install 'virtualenv'
pip3 install virtualenv

# Use'virtualenv' to provision a virtual environment
virtualenv -p python3 --no-site-packages run/lib

# Instantiate a virtual environment
source run/lib/bin/activate

# Recurseively install this project's dependencies
pip3 install -r setup/requirements.txt