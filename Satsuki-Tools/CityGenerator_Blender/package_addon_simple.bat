@echo off
cls
echo ===============================================
echo     CITY BLOCK GENERATOR - PACKAGING TOOL
echo ===============================================
echo.

REM Supprimer l'ancien ZIP s'il existe
if exist "city_block_generator_6_12.zip" (
    echo [Suppression] Ancien fichier ZIP trouve, suppression...
    del "city_block_generator_6_12.zip"
    echo [OK] Ancien ZIP supprime
) else (
    echo [INFO] Aucun ancien ZIP a supprimer
)

echo.
echo [CREATION] Compression du dossier en cours...

REM Utiliser PowerShell pour créer le ZIP
powershell -Command "Compress-Archive -Path 'city_block_generator_6_12' -DestinationPath 'city_block_generator_6_12.zip' -CompressionLevel Optimal -Force"

if %errorlevel% equ 0 (
    echo [SUCCES] Package cree avec succes !
    echo.
    echo FICHIER PRET: city_block_generator_6_12.zip
    echo.
    echo INSTRUCTIONS D'INSTALLATION:
    echo 1. Ouvrez Blender
    echo 2. Edit ^> Preferences ^> Add-ons
    echo 3. Install ^> Selectionnez le fichier ZIP
    echo 4. Activez 'City Block Generator'
    echo 5. Version installee: voir __init__.py pour la version actuelle
    echo.
    echo ===============================================
) else (
    echo [ERREUR] Echec de la creation du package
)

echo.
pause
