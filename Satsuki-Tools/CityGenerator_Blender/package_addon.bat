@echo off
setlocal EnableDelayedExpansion

REM Script Batch pour packager l'addon City Block Generator
REM Supprime l'ancien ZIP et crée un nouveau package

echo === PACKAGING CITY BLOCK GENERATOR ADDON ===
echo.

REM Configuration
set "ZIP_NAME=city_block_generator_6_12.zip"
set "ADDON_DIR=city_block_generator_6_12"
set "INIT_FILE=%ADDON_DIR%\__init__.py"

REM Vérifier si le dossier de l'addon existe
if not exist "%ADDON_DIR%" (
    echo [91mERREUR: Le dossier '%ADDON_DIR%' n'existe pas![0m
    echo [93m   Assurez-vous d'être dans le bon répertoire.[0m
    pause
    exit /b 1
)

echo [92mDossier source trouvé: %ADDON_DIR%[0m

REM Lire la version depuis __init__.py
set "ADDON_VERSION=version inconnue"
if exist "%INIT_FILE%" (
    for /f "delims=" %%i in ('powershell -Command "(Get-Content '%INIT_FILE%' | Select-String 'version.*(\d+),\s*(\d+),\s*(\d+)' | ForEach-Object {$_.Matches[0].Groups[1].Value + '.' + $_.Matches[0].Groups[2].Value + '.' + $_.Matches[0].Groups[3].Value})"') do (
        set "ADDON_VERSION=%%i"
    )
    if not "!ADDON_VERSION!"=="version inconnue" (
        echo [92mVersion détectée: !ADDON_VERSION![0m
    ) else (
        echo [93mAVERTISSEMENT: Version non trouvée dans __init__.py[0m
    )
) else (
    echo [93mAVERTISSEMENT: Fichier __init__.py non trouvé[0m
)

REM Supprimer l'ancien fichier ZIP s'il existe
if exist "%ZIP_NAME%" (
    echo [93mSuppression de l'ancien fichier: %ZIP_NAME%[0m
    del "%ZIP_NAME%" >nul 2>&1
    if !errorlevel! equ 0 (
        echo [92m   Ancien ZIP supprimé avec succès[0m
    ) else (
        echo [91m   Erreur lors de la suppression[0m
        pause
        exit /b 1
    )
) else (
    echo [94mAucun ancien ZIP à supprimer[0m
)

echo.
echo [96mCréation du nouveau package...[0m
echo [90m   Source: %ADDON_DIR%\[0m
echo [90m   Destination: %ZIP_NAME%[0m

REM Créer le fichier ZIP en utilisant PowerShell (disponible sur Windows 10+)
powershell -Command "Compress-Archive -Path '%ADDON_DIR%' -DestinationPath '%ZIP_NAME%' -CompressionLevel Optimal -Force"

if !errorlevel! equ 0 (
    echo.
    echo [92mSUCCÈS! Package créé: %ZIP_NAME%[0m
    
    REM Afficher la taille du fichier
    for %%F in ("%ZIP_NAME%") do (
        set "file_size=%%~zF"
        set /a "size_kb=!file_size!/1024"
        echo [90m   Taille du fichier: !size_kb! KB[0m
    )
    
    echo.
    echo [92mPRÊT POUR L'INSTALLATION:[0m
    echo [97m   1. Ouvrez Blender[0m
    echo [97m   2. Edit ^> Preferences ^> Add-ons[0m
    echo [97m   3. Install ^> Sélectionnez %ZIP_NAME%[0m
    echo [97m   4. Activez 'City Block Generator'[0m
    echo [93m   5. Version: !ADDON_VERSION![0m
) else (
    echo.
    echo [91mERREUR lors de la création du package![0m
    pause
    exit /b 1
)

echo.
echo === PACKAGING TERMINÉ ===
echo.
echo Appuyez sur une touche pour continuer...
pause >nul
