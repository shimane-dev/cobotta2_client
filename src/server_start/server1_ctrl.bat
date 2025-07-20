@echo off

REM Python.exe の絶対パス（例: C:\Users\USER\AppData\Local\Programs\Python\Python311\python.exe）
REM Get-Command python | Select-Object -ExpandProperty Source
set PYTHON_PATH=C:\Users\nakada\AppData\Local\Programs\Python\Python313\python.exe

REM server1_ctrl.py の絶対パス
set SCRIPT_PATH=C:\Users\nakada\zaiene_dev\cobotta2\examples\server1_ctrl.py

REM サービス名
set SERVICE_NAME=COBOTTA_Server

REM nssm.exe の絶対パス
set NSSM_PATH=C:\tools\nssm.exe
REM ========== ユーザー設定ここまで ==========

REM サービス登録
"%NSSM_PATH%" install %SERVICE_NAME% "%PYTHON_PATH%" "%SCRIPT_PATH%"

REM 起動ディレクトリをスクリプトの場所に設定（必要に応じて）
"%NSSM_PATH%" set %SERVICE_NAME% AppDirectory C:\path\to\your

REM 必要ならサービス起動
net start %SERVICE_NAME%
