@echo off
echo ============================================================
echo MATANDO PROCESO EN PUERTO 8000
echo ============================================================
echo.

REM Buscar el proceso en el puerto 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    set PID=%%a
    goto :found
)

echo No se encontro ningun proceso en el puerto 8000
echo El puerto esta libre.
pause
exit /b

:found
echo Proceso encontrado: PID %PID%
echo Terminando proceso...
taskkill /F /PID %PID%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo OK Proceso terminado exitosamente!
    echo El puerto 8000 esta ahora libre.
) else (
    echo.
    echo X Error al terminar el proceso.
)

echo.
pause

