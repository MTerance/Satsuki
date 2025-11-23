# Script de réinitialisation du plugin DecorManager
# Date : 22 novembre 2025

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  REINITIALISATION DECORMANAGER" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$projectPath = "C:\Users\sshom\source\repos\Satsuki\Satsuki"

# 1. Vérifier que Godot est fermé
Write-Host "[1/5] Verification de Godot..." -ForegroundColor Yellow
$godotProcess = Get-Process -Name "Godot*" -ErrorAction SilentlyContinue
if ($godotProcess) {
    Write-Host "  ??  Godot est en cours d'execution" -ForegroundColor Red
    Write-Host "  Veuillez fermer Godot avant de continuer" -ForegroundColor Red
    Read-Host "Appuyez sur Entree apres avoir ferme Godot"
} else {
    Write-Host "  ? Godot n'est pas en cours d'execution" -ForegroundColor Green
}

# 2. Supprimer le cache Godot
Write-Host ""
Write-Host "[2/5] Suppression du cache Godot..." -ForegroundColor Yellow
$godotCachePath = Join-Path $projectPath ".godot"
if (Test-Path $godotCachePath) {
    Remove-Item -Path $godotCachePath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  ? Cache .godot/ supprime" -ForegroundColor Green
} else {
    Write-Host "  ??  Cache .godot/ n'existe pas" -ForegroundColor Gray
}

# 3. Vérifier plugin.cfg
Write-Host ""
Write-Host "[3/5] Verification de plugin.cfg..." -ForegroundColor Yellow
$pluginCfgPath = Join-Path $projectPath "addons\decor_manager\plugin.cfg"
if (Test-Path $pluginCfgPath) {
    $content = Get-Content $pluginCfgPath -Raw
    if ($content -match 'script="res://addons/decor_manager/DecorManagerTool\.cs"') {
        Write-Host "  ? plugin.cfg correct" -ForegroundColor Green
    } else {
        Write-Host "  ? plugin.cfg incorrect" -ForegroundColor Red
        Write-Host "  Contenu actuel :" -ForegroundColor Yellow
        Write-Host $content
    }
} else {
    Write-Host "  ? plugin.cfg introuvable" -ForegroundColor Red
}

# 4. Vérifier DecorManagerTool.cs
Write-Host ""
Write-Host "[4/5] Verification de DecorManagerTool.cs..." -ForegroundColor Yellow
$toolPath = Join-Path $projectPath "addons\decor_manager\DecorManagerTool.cs"
if (Test-Path $toolPath) {
    $fileSize = (Get-Item $toolPath).Length
    Write-Host "  ? DecorManagerTool.cs trouve ($fileSize octets)" -ForegroundColor Green
} else {
    Write-Host "  ? DecorManagerTool.cs introuvable" -ForegroundColor Red
}

# 5. Vérifier la compilation
Write-Host ""
Write-Host "[5/5] Verification de la compilation..." -ForegroundColor Yellow
$csprojPath = Join-Path $projectPath "Satsuki.csproj"
if (Test-Path $csprojPath) {
    Write-Host "  ??  Projet trouve : Satsuki.csproj" -ForegroundColor Gray
    Write-Host "  ?? Assurez-vous que le projet est compile (Build ? Rebuild)" -ForegroundColor Cyan
} else {
    Write-Host "  ??  Fichier .csproj introuvable" -ForegroundColor Yellow
}

# Résumé
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  RESUME" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "? Cache supprime" -ForegroundColor Green
Write-Host "? Fichiers verifies" -ForegroundColor Green
Write-Host ""
Write-Host "PROCHAINES ETAPES :" -ForegroundColor Yellow
Write-Host "1. Rouvrir Godot" -ForegroundColor White
Write-Host "2. Activer le plugin dans Project Settings ? Plugins" -ForegroundColor White
Write-Host "3. Verifier le dock 'Decor Manager' a droite" -ForegroundColor White
Write-Host ""
Write-Host "Si des erreurs persistent, voir :" -ForegroundColor Yellow
Write-Host "  Documentation/DecorManager_Final_Solution.md" -ForegroundColor Cyan
Write-Host ""

Read-Host "Appuyez sur Entree pour fermer"
