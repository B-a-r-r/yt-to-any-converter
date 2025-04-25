#!/bin/bash

if [ ! -d .venv ]; then
  echo "Environnement virtuel introuvable, veuillez lancer setup.bat avant de continuer."
  exit
fi

source .venv/bin/activate

python ./main.py 

deactivate