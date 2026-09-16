@echo off
setlocal EnableExtensions
title EcoTech - Instalacao
cd /d "%~dp0"

echo ==============================================
echo       ECOTECH v1.0.3 - INSTALACAO LOCAL
echo ==============================================
echo.

set "PY_CMD="
where python >nul 2>nul
if %errorlevel%==0 (
    for /f "tokens=2" %%V in ('python --version 2^>^&1') do set "PY_VERSION=%%V"
    set "PY_CMD=python"
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        py -3.13 --version >nul 2>nul
        if %errorlevel%==0 set "PY_CMD=py -3.13"
    )
)

if not defined PY_CMD (
    echo [ERRO] Python nao foi encontrado.
    echo Este projeto foi homologado para Python 3.13.x.
    echo Verifique no CMD: python --version
    pause
    exit /b 1
)

echo Python detectado:
%PY_CMD% --version
%PY_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3,13) else 1)"
if errorlevel 1 (
    echo [ERRO] E necessario Python 3.13 ou superior.
    pause
    exit /b 1
)

echo.
if not exist "venv\Scripts\python.exe" (
    echo [1/8] Criando ambiente virtual...
    %PY_CMD% -m venv venv
    if errorlevel 1 goto :erro
) else (
    echo [1/8] Ambiente virtual existente encontrado.
)

call "venv\Scripts\activate.bat"
if errorlevel 1 goto :erro

echo [2/8] Atualizando pip...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 goto :erro

echo [3/8] Instalando dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 goto :erro

echo [4/8] Gerando migracoes do projeto...
python manage.py makemigrations accounts residuos coletas pontos notificacoes auditoria --noinput
if errorlevel 1 goto :erro

echo [5/8] Aplicando migracoes...
python manage.py migrate --noinput
if errorlevel 1 goto :erro

echo [6/8] Carregando base demonstrativa...
python manage.py seed_demo
if errorlevel 1 goto :erro

echo [7/8] Coletando arquivos estaticos...
python manage.py collectstatic --noinput
if errorlevel 1 goto :erro

echo [8/8] Validando Django...
python manage.py check
if errorlevel 1 goto :erro

echo.
echo ==============================================
echo      INSTALACAO CONCLUIDA COM SUCESSO
echo ==============================================
echo Acesso: http://127.0.0.1:8000/
echo Usuario: joao / EcoTech@2026
echo Admin:   admin / EcoTech@2026
echo.
echo Agora execute Executar.bat
pause
exit /b 0

:erro
echo.
echo ==============================================
echo [ERRO] A INSTALACAO FOI INTERROMPIDA
echo ==============================================
echo O instalador nao marcou a instalacao como concluida.
echo Revise a mensagem imediatamente acima.
pause
exit /b 1
