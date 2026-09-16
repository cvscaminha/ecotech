@echo off
setlocal
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
 echo [ERRO] Execute Instalar.bat primeiro.
 pause
 exit /b 1
)
call "venv\Scripts\activate.bat"
python manage.py check
if errorlevel 1 goto :erro
python manage.py test
if errorlevel 1 goto :erro
echo.
echo TODOS OS TESTES FORAM CONCLUIDOS.
pause
exit /b 0
:erro
echo.
echo [ERRO] A validacao encontrou problemas.
pause
exit /b 1
