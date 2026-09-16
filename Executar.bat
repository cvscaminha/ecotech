@echo off
setlocal
title EcoTech - Execucao
cd /d "%~dp0"

echo ==============================================
echo ECOTECH - INICIANDO SISTEMA
echo ==============================================

if not exist "venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual nao encontrado.
    echo Execute Instalar.bat primeiro.
    pause
    exit /b 1
)

call "venv\Scripts\activate.bat"
if errorlevel 1 goto :erro

python manage.py check
if errorlevel 1 goto :erro

start "" "http://127.0.0.1:8000/dashboard/"

echo.
echo ==============================================
echo EcoTech iniciado: http://127.0.0.1:8000/dashboard/
echo Para encerrar o servidor pressione CTRL+C.
echo ==============================================

python manage.py runserver 0.0.0.0:8000
exit /b %errorlevel%

:erro
echo [ERRO] O EcoTech nao passou na verificacao do Django.
pause
exit /b 1
