#!/bin/bash

if [ "$(id -u)" != "0" ]; then
  echo "Vous devez executer ce script en mode administrateur."
  exit 1
fi

wget https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
chmod +x python-3.9.7-amd64.exe
./python-3.9.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

python -m ensurepip

python -m venv .venv

pip install -r requirements.txt