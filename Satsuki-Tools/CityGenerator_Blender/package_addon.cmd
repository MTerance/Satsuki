@echo off
title City Block Generator - Package Creator

echo.
echo ================================
echo  CITY BLOCK GENERATOR PACKAGER
echo ================================
echo.

echo Suppression ancien ZIP...
if exist city_block_generator_6_12.zip del city_block_generator_6_12.zip

echo Creation du nouveau package...
powershell -Command "Compress-Archive -Path 'city_block_generator_6_12' -DestinationPath 'city_block_generator_6_12.zip' -Force" >nul 2>&1

if exist city_block_generator_6_12.zip (
    echo.
    echo [SUCCES] Package cree !
    echo.
    echo Fichier: city_block_generator_6_12.zip
    echo Version: 6.12.7 ^(corrigee^)
    echo.
    echo INSTALLATION:
    echo 1. Ouvrir Blender
    echo 2. Edit ^> Preferences ^> Add-ons
    echo 3. Install ^> city_block_generator_6_12.zip
    echo 4. Activer l'addon
) else (
    echo [ERREUR] Echec creation package
)

echo.
echo ================================
pause
