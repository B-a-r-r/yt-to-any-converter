@echo off

if not exist .venv (
  echo Environnement virtuel introuvable, veuillez lancer setup.bat avant de continuer.
  pause
  exit
)

call .venv\Scripts\activate

python ./main.py 

call .venv\Scripts\deactivate