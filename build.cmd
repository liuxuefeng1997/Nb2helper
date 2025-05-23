@echo off
chcp 65001
set
cd %`dp0
.\.venv\Scripts\pyinstaller.exe Nb2helper.spec
