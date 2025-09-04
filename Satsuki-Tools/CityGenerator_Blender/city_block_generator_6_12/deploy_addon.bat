@echo off
echo 🚀 Deploiement de l'addon City Block Generator...
echo.

REM Obtenir le répertoire du script
set SCRIPT_DIR=%~dp0

REM Exécuter le script PowerShell
powershell.exe -ExecutionPolicy Bypass -File "%SCRIPT_DIR%deploy_addon.ps1" %*

REM Pause pour voir les résultats
pause
