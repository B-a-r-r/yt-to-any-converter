@echo off

openfiles > NUL 2>&1
if %errorlevel%==0 (
    echo Vous devez executer ce script en mode administrateur.
    pause
    exit
)

powershell -Command "Invoke-WebRequest -Uri [https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe](https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe) -OutFile python-3.9.7-amd64.exe"
start /wait python-3.9.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

powershell -Command "python -m ensurepip"

python -m venv .venv

call .venv\Scripts\activate

pip install -r requirements.txt

python --version
pip --version

echo Installation réussie !
pause