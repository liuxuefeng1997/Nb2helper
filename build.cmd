@echo off
chcp 65001
set
cd %`dp0
.\.venv\Scripts\pyinstaller.exe -F -w Main.py -n Nb2helper -i resources\icon.ico --add-data ".\\resources\\*.*;.\\resources"
