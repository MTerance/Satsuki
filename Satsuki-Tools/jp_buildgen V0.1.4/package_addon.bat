@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  JP Building Generator - Package Creator
echo ========================================
echo.

REM Configuration
set ADDON_NAME=jp_buildgen
set VERSION=0.1.4
set ZIP_NAME=%ADDON_NAME%_v%VERSION%.zip
set SOURCE_DIR=%~dp0
set TEMP_DIR=%TEMP%\%ADDON_NAME%_package
set EXCLUDE_FILES=*.bat *.md CORRECTION_FLOTTEMENT.md __pycache__ *.pyc

echo Source directory: %SOURCE_DIR%
echo Package name: %ZIP_NAME%
echo.

REM Nettoyer le répertoire temporaire
if exist "%TEMP_DIR%" (
    echo Cleaning temporary directory...
    rmdir /s /q "%TEMP_DIR%"
)

REM Créer le répertoire temporaire
echo Creating temporary package directory...
mkdir "%TEMP_DIR%"
mkdir "%TEMP_DIR%\%ADDON_NAME%"

REM Copier les fichiers nécessaires
echo Copying addon files...
copy "%SOURCE_DIR%__init__.py" "%TEMP_DIR%\%ADDON_NAME%\" >nul
copy "%SOURCE_DIR%core.py" "%TEMP_DIR%\%ADDON_NAME%\" >nul
copy "%SOURCE_DIR%operators.py" "%TEMP_DIR%\%ADDON_NAME%\" >nul
copy "%SOURCE_DIR%panels.py" "%TEMP_DIR%\%ADDON_NAME%\" >nul
copy "%SOURCE_DIR%properties.py" "%TEMP_DIR%\%ADDON_NAME%\" >nul
copy "%SOURCE_DIR%README.md" "%TEMP_DIR%\%ADDON_NAME%\" >nul

REM Copier le dossier textures
echo Copying textures directory...
xcopy "%SOURCE_DIR%textures" "%TEMP_DIR%\%ADDON_NAME%\textures" /e /i /q >nul

REM Créer le ZIP en utilisant PowerShell
echo Creating ZIP package...
powershell -command "Compress-Archive -Path '%TEMP_DIR%\%ADDON_NAME%' -DestinationPath '%SOURCE_DIR%%ZIP_NAME%' -Force"

REM Nettoyer le répertoire temporaire
echo Cleaning up...
rmdir /s /q "%TEMP_DIR%"

REM Vérifier si le ZIP a été créé
if exist "%SOURCE_DIR%%ZIP_NAME%" (
    echo.
    echo ========================================
    echo  SUCCESS! Package created successfully
    echo ========================================
    echo.
    echo Package: %ZIP_NAME%
    echo Location: %SOURCE_DIR%
    echo.
    echo To install in Blender:
    echo 1. Open Blender
    echo 2. Go to Edit ^> Preferences ^> Add-ons
    echo 3. Click "Install..." button
    echo 4. Select the %ZIP_NAME% file
    echo 5. Enable the "JP Building Generator" addon
    echo.
) else (
    echo.
    echo ========================================
    echo  ERROR! Failed to create package
    echo ========================================
    echo.
)

pause