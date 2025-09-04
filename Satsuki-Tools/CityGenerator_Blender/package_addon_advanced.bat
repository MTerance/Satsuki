@echo off
setlocal enabledelayedexpansion
cls
echo ===============================================
echo     CITY BLOCK GENERATOR - PACKAGING TOOL
echo ===============================================
echo.

set "ADDON_DIR=city_block_generator_6_12"
set "ZIP_NAME=city_block_generator_6_12.zip"
set "INIT_FILE=%ADDON_DIR%\__init__.py"
set "ADDON_VERSION=version inconnue"

REM Lire la version depuis __init__.py
if exist "%INIT_FILE%" (
    echo [INFO] Lecture de la version depuis %INIT_FILE%...
    for /f "tokens=*" %%i in ('findstr "version.*(" "%INIT_FILE%"') do (
        set "version_line=%%i"
        for /f "tokens=2,3,4 delims=(),: " %%a in ("!version_line!") do (
            set "ADDON_VERSION=%%a.%%b.%%c"
        )
    )
    echo [OK] Version detectee: !ADDON_VERSION!
) else (
    echo [ERREUR] Fichier %INIT_FILE% non trouve
)
echo.

REM Supprimer l'ancien ZIP s'il existe
if exist "%ZIP_NAME%" (
    echo [Suppression] Ancien fichier ZIP trouve, suppression...
    del "%ZIP_NAME%"
    echo [OK] Ancien ZIP supprime
) else (
    echo [INFO] Aucun ancien ZIP a supprimer
)

echo.
echo [CREATION] Compression du dossier en cours...

REM Utiliser PowerShell pour créer le ZIP
powershell -Command "Compress-Archive -Path '%ADDON_DIR%' -DestinationPath '%ZIP_NAME%' -CompressionLevel Optimal -Force"

if %errorlevel% equ 0 (
    echo [SUCCES] Package cree avec succes !
    echo.
    echo FICHIER PRET: %ZIP_NAME%
    echo.
    echo INSTRUCTIONS D'INSTALLATION:
    echo 1. Ouvrez Blender
    echo 2. Edit ^> Preferences ^> Add-ons
    echo 3. Install ^> Selectionnez le fichier ZIP
    echo 4. Activez 'City Block Generator'
    echo 5. Version installee: !ADDON_VERSION!
    echo.
    echo ===============================================
) else (
    echo [ERREUR] Echec de la creation du package
)

echo.
pause
