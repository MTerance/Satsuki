# Script de nettoyage complet pour résoudre le problème de chemin dupliqué
# Date : 22 novembre 2025

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  NETTOYAGE COMPLET DECORMANAGER" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$projectPath = "C:\Users\sshom\source\repos\Satsuki\Satsuki"

# 1. Fermer Godot
Write-Host "[1/4] Verification que Godot est ferme..." -ForegroundColor Yellow
$godotProcess = Get-Process -Name "Godot*" -ErrorAction SilentlyContinue
if ($godotProcess) {
    Write-Host "  ATTENTION: Godot est en cours d'execution!" -ForegroundColor Red
    Write-Host "  Fermeture de Godot..." -ForegroundColor Yellow
    $godotProcess | Stop-Process -Force
    Start-Sleep -Seconds 2
    Write-Host "  Godot ferme" -ForegroundColor Green
} else {
    Write-Host "  OK: Godot n'est pas en cours d'execution" -ForegroundColor Green
}

# 2. Supprimer TOUS les caches
Write-Host ""
Write-Host "[2/4] Suppression de tous les caches..." -ForegroundColor Yellow

# Cache .godot
$godotCache = Join-Path $projectPath ".godot"
if (Test-Path $godotCache) {
    Remove-Item -Path $godotCache -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  Cache .godot/ supprime" -ForegroundColor Green
}

# Cache import
$importCache = Join-Path $projectPath ".godot\imported"
if (Test-Path $importCache) {
    Remove-Item -Path $importCache -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  Cache imports supprime" -ForegroundColor Green
}

# Cache editor
$editorCache = Join-Path $projectPath ".godot\editor"
if (Test-Path $editorCache) {
    Remove-Item -Path $editorCache -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  Cache editor supprime" -ForegroundColor Green
}

# Fichiers .import
Get-ChildItem -Path $projectPath -Filter "*.import" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "  Fichiers .import supprimes" -ForegroundColor Green

Write-Host "  Tous les caches supprimes!" -ForegroundColor Green

# 3. Vérifier et corriger plugin.cfg
Write-Host ""
Write-Host "[3/4] Verification de plugin.cfg..." -ForegroundColor Yellow

$pluginCfg = Join-Path $projectPath "addons\decor_manager\plugin.cfg"
$expectedContent = @"
[plugin]

name="Decor Manager"
description="Outil de gestion des decors et cameras pour Satsuki"
author="Satsuki Team"
version="1.0"
script="res://addons/decor_manager/DecorManagerTool.cs"
"@

# Supprimer et recréer le fichier
if (Test-Path $pluginCfg) {
    Remove-Item $pluginCfg -Force
}

# Créer le nouveau fichier avec encodage UTF-8 sans BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($pluginCfg, $expectedContent, $utf8NoBom)

Write-Host "  plugin.cfg recree avec succes" -ForegroundColor Green
Write-Host "  Contenu:" -ForegroundColor Cyan
Write-Host $expectedContent -ForegroundColor Gray

# 4. Vérifier DecorManagerTool.cs
Write-Host ""
Write-Host "[4/4] Verification de DecorManagerTool.cs..." -ForegroundColor Yellow

$toolPath = Join-Path $projectPath "addons\decor_manager\DecorManagerTool.cs"
if (Test-Path $toolPath) {
    $fileSize = (Get-Item $toolPath).Length
    Write-Host "  DecorManagerTool.cs present ($fileSize octets)" -ForegroundColor Green
} else {
    Write-Host "  ERREUR: DecorManagerTool.cs manquant!" -ForegroundColor Red
}

# Résumé final
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  NETTOYAGE TERMINE" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PROCHAINES ETAPES:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Rouvrir Godot" -ForegroundColor White
Write-Host "2. Attendre la regeneration complete du cache" -ForegroundColor White
Write-Host "3. Aller dans: Project -> Project Settings -> Plugins" -ForegroundColor White
Write-Host "4. Activer 'Decor Manager'" -ForegroundColor White
Write-Host ""
Write-Host "Le plugin devrait maintenant fonctionner!" -ForegroundColor Green
Write-Host ""

Read-Host "Appuyez sur Entree pour fermer"
