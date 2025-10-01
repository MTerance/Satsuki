@echo off
REM Version simple et rapide
set ZIP_NAME=jp_buildgen_v0.1.4.zip
set TEMP_DIR=%TEMP%\jp_buildgen_package

echo Creating %ZIP_NAME%...

REM Supprimer l'ancien ZIP s'il existe
if exist "%ZIP_NAME%" del "%ZIP_NAME%"

REM Nettoyer et créer le répertoire temporaire
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"
mkdir "%TEMP_DIR%\jp_buildgen"

REM Copier les fichiers dans le dossier temporaire
echo Copying files...
copy "__init__.py" "%TEMP_DIR%\jp_buildgen\" >nul
copy "core.py" "%TEMP_DIR%\jp_buildgen\" >nul
copy "operators.py" "%TEMP_DIR%\jp_buildgen\" >nul
copy "panels.py" "%TEMP_DIR%\jp_buildgen\" >nul
copy "properties.py" "%TEMP_DIR%\jp_buildgen\" >nul
copy "README.md" "%TEMP_DIR%\jp_buildgen\" >nul
xcopy "textures" "%TEMP_DIR%\jp_buildgen\textures" /e /i /q >nul

REM Créer le ZIP avec la structure correcte
powershell -command "Compress-Archive -Path '%TEMP_DIR%\jp_buildgen' -DestinationPath '%ZIP_NAME%' -Force"

REM Nettoyer le répertoire temporaire
rmdir /s /q "%TEMP_DIR%"

if exist "%ZIP_NAME%" (
    echo SUCCESS: %ZIP_NAME% created!
    echo Ready for Blender installation.
) else (
    echo ERROR: Failed to create package.
)

pause