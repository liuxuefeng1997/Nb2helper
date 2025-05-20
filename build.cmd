@echo off
chcp 65001
set
cd %`dp0
.\.venv\Scripts\pyinstaller.exe -F Main.py -n Nb2helper -i icon.ico
