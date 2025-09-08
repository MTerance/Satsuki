@echo off
echo 🔧 VERIFICATION RAPIDE BLENDER
echo ================================
echo.

echo 📦 Verification installation...
if exist "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" (
    echo ✅ Blender trouve
) else (
    echo ❌ Blender non trouve
    goto :error
)

echo.
echo 🧪 Test de lancement...
"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --version > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Blender fonctionne
) else (
    echo ❌ Probleme lancement Blender
    goto :solutions
)

echo.
echo 🌊 Verification addon organique...
if exist "c:\Users\sshom\Documents\assets\Tools\tokyo_organic_1_1_0\__init__.py" (
    echo ✅ Addon organique disponible
) else (
    echo ❌ Addon organique manquant
    goto :error
)

echo.
echo 🎉 TOUT FONCTIONNE PARFAITEMENT!
echo.
echo 🚀 Voulez-vous lancer Blender maintenant? (O/N)
set /p choice=Votre choix: 
if /i "%choice%"=="O" (
    echo ⏳ Lancement Blender...
    start "" "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
    echo ✅ Blender lance!
)
goto :end

:solutions
echo.
echo 🛠️ SOLUTIONS DE DEPANNAGE:
echo.
echo 1. Factory reset:
echo    "C:\Program Files\Blender Foundation\Blender 4.5\blender_factory_startup.cmd"
echo.
echo 2. Mode debug:
echo    "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --debug
echo.
echo 3. Redemarrer Windows
echo.
echo 4. Tuer processus Blender:
echo    taskkill /f /im blender.exe
echo.
goto :end

:error
echo.
echo ❌ PROBLEME DETECTE!
echo 📖 Consultez GUIDE_DEPANNAGE_BLENDER.md pour les solutions
echo.

:end
echo.
echo 📖 Guide complet: GUIDE_DEPANNAGE_BLENDER.md
echo 🌊 Addon organique: tokyo_organic_1_1_0
echo.
pause
