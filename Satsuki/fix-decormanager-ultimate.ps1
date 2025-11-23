# Solution ultime pour le problème de chemin dupliqué
# Ce script va tout nettoyer de manière agressive

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "  SOLUTION ULTIME - DECORMANAGER" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

$projectPath = "C:\Users\sshom\source\repos\Satsuki\Satsuki"

# 1. Force-kill tous les processus Godot
Write-Host "[1/6] Arret force de tous les processus Godot..." -ForegroundColor Yellow
Get-Process -Name "*Godot*" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process -Name "*godot*" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2
Write-Host "  Tous les processus Godot arretes" -ForegroundColor Green

# 2. Supprimer TOUT le cache Godot
Write-Host ""
Write-Host "[2/6] Suppression COMPLETE du cache..." -ForegroundColor Yellow
$paths = @(
    ".godot",
    ".godot\imported",
    ".godot\editor",
    ".godot\mono",
    ".mono",
    ".import"
)

foreach ($path in $paths) {
    $fullPath = Join-Path $projectPath $path
    if (Test-Path $fullPath) {
        Remove-Item -Path $fullPath -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  $path supprime" -ForegroundColor Green
    }
}

# Supprimer tous les .import
Get-ChildItem -Path $projectPath -Filter "*.import" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force
Write-Host "  Tous les fichiers .import supprimes" -ForegroundColor Green

# 3. Supprimer le plugin complètement
Write-Host ""
Write-Host "[3/6] Suppression complete du plugin..." -ForegroundColor Yellow
$addonPath = Join-Path $projectPath "addons\decor_manager"
if (Test-Path $addonPath) {
    Remove-Item -Path $addonPath -Recurse -Force
    Write-Host "  Plugin supprime" -ForegroundColor Green
}

# 4. Recréer le plugin proprement
Write-Host ""
Write-Host "[4/6] Recreation du plugin..." -ForegroundColor Yellow

# Créer le dossier
New-Item -Path $addonPath -ItemType Directory -Force | Out-Null

# Créer plugin.cfg
$pluginCfg = @"
[plugin]

name="Decor Manager"
description="Outil de gestion des decors et cameras pour Satsuki"
author="Satsuki Team"
version="1.0"
script="res://addons/decor_manager/DecorManagerTool.cs"
"@

$pluginCfgPath = Join-Path $addonPath "plugin.cfg"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($pluginCfgPath, $pluginCfg, $utf8NoBom)
Write-Host "  plugin.cfg cree" -ForegroundColor Green

# 5. Copier DecorManagerTool.cs depuis Tools/
Write-Host ""
Write-Host "[5/6] Copie de DecorManagerTool.cs..." -ForegroundColor Yellow
$sourceFile = Join-Path $projectPath "Tools\DecorManagerTool.cs"
$destFile = Join-Path $addonPath "DecorManagerTool.cs"

if (Test-Path $sourceFile) {
    # Lire le contenu
    $content = Get-Content $sourceFile -Raw -Encoding UTF8
    
    # S'assurer qu'il commence par using Godot;
    if (-not $content.StartsWith("using Godot;")) {
        $content = "using Godot;`n" + $content
    }
    
    # Écrire avec UTF-8 sans BOM
    [System.IO.File]::WriteAllText($destFile, $content, $utf8NoBom)
    Write-Host "  DecorManagerTool.cs copie" -ForegroundColor Green
} else {
    Write-Host "  ERREUR: Tools\DecorManagerTool.cs introuvable!" -ForegroundColor Red
    Write-Host "  Le fichier doit etre cree manuellement" -ForegroundColor Red
}

# 6. Nettoyer le cache utilisateur Godot
Write-Host ""
Write-Host "[6/6] Nettoyage du cache utilisateur Godot..." -ForegroundColor Yellow
$godotConfigPath = "$env:APPDATA\Godot"
if (Test-Path $godotConfigPath) {
    $editorCache = Join-Path $godotConfigPath "editor_cache"
    if (Test-Path $editorCache) {
        Remove-Item -Path $editorCache -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  Cache utilisateur Godot supprime" -ForegroundColor Green
    }
}

# Résumé
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  NETTOYAGE COMPLET TERMINE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "VERIFICATIONS:" -ForegroundColor Yellow
Write-Host ""

# Vérifier plugin.cfg
if (Test-Path $pluginCfgPath) {
    Write-Host "plugin.cfg:" -ForegroundColor Cyan
    Get-Content $pluginCfgPath | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
} else {
    Write-Host "ERREUR: plugin.cfg manquant!" -ForegroundColor Red
}

Write-Host ""

# Vérifier DecorManagerTool.cs
if (Test-Path $destFile) {
    $size = (Get-Item $destFile).Length
    Write-Host "DecorManagerTool.cs: OK ($size octets)" -ForegroundColor Green
} else {
    Write-Host "ERREUR: DecorManagerTool.cs manquant!" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PROCHAINES ETAPES OBLIGATOIRES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "OPTION A (Recommandee):" -ForegroundColor Yellow
Write-Host "1. REDEMARRER WINDOWS" -ForegroundColor White
Write-Host "2. Rouvrir Godot" -ForegroundColor White
Write-Host "3. Activer le plugin" -ForegroundColor White
Write-Host ""
Write-Host "OPTION B (Si vous ne pouvez pas redemarrer):" -ForegroundColor Yellow
Write-Host "1. Rouvrir Godot" -ForegroundColor White
Write-Host "2. Si erreur persiste -> REDEMARRER WINDOWS" -ForegroundColor White
Write-Host ""

Read-Host "Appuyez sur Entree pour fermer"
