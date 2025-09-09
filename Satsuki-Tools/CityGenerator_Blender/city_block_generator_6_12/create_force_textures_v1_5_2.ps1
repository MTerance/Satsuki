# Script PowerShell pour créer tokyo_city_generator_v1_5_2_force_textures.zip

Write-Host "CREATION TOKYO CITY GENERATOR v1.5.2 FORCE TEXTURES" -ForegroundColor Green

$projectRoot = $PSScriptRoot
$addonSource = Join-Path $projectRoot "TOKYO_ADDON_1_0"
$zipName = "tokyo_city_generator_v1_5_2_force_textures.zip"
$zipPath = Join-Path $projectRoot $zipName

# Supprimer ancien ZIP
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
    Write-Host "Ancien ZIP supprimé" -ForegroundColor Yellow
}

# Vérifier fichiers
Write-Host "Vérification fichiers..." -ForegroundColor Yellow
$initFile = Join-Path $addonSource "__init__.py"
$textureFile = Join-Path $addonSource "texture_system.py"

if (Test-Path $initFile) {
    $size1 = (Get-Item $initFile).Length
    Write-Host "__init__.py: $size1 bytes" -ForegroundColor Green
} else {
    Write-Error "__init__.py manquant"
    exit 1
}

if (Test-Path $textureFile) {
    $size2 = (Get-Item $textureFile).Length
    Write-Host "texture_system.py: $size2 bytes" -ForegroundColor Green
} else {
    Write-Error "texture_system.py manquant"
    exit 1
}

# Vérifier contenu spécifique v1.5.2
$content = Get-Content $initFile -Raw
if ($content -match "TOKYO_OT_force_apply_textures") {
    Write-Host "✓ Opérateur force textures détecté" -ForegroundColor Green
} else {
    Write-Warning "Opérateur force textures manquant"
}

if ($content -match "version.*1.*5.*2") {
    Write-Host "✓ Version 1.5.2 détectée" -ForegroundColor Green
} else {
    Write-Warning "Version 1.5.2 non détectée"
}

# Créer ZIP
try {
    Write-Host "Création ZIP..." -ForegroundColor Yellow
    
    $tempDir = Join-Path $env:TEMP "tokyo_force_textures"
    $addonDir = Join-Path $tempDir "tokyo_city_generator"
    
    if (Test-Path $tempDir) {
        Remove-Item $tempDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $addonDir -Force | Out-Null
    
    Copy-Item $initFile $addonDir -Force
    Copy-Item $textureFile $addonDir -Force
    
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $zipPath)
    
    Remove-Item $tempDir -Recurse -Force
    
    Write-Host "ZIP créé!" -ForegroundColor Green
    
} catch {
    Write-Error "Erreur: $_"
    exit 1
}

# Vérifier résultat
if (Test-Path $zipPath) {
    $zipSize = (Get-Item $zipPath).Length
    Write-Host "ZIP final: $zipSize bytes" -ForegroundColor Cyan
    Write-Host "Fichier: $zipName" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "NOUVEAUTÉS v1.5.2:" -ForegroundColor Magenta
    Write-Host "- Bouton Force Application Textures" -ForegroundColor Green
    Write-Host "- Application automatique sur bâtiments existants" -ForegroundColor Green
    Write-Host "- Remplacement des matériaux par défaut" -ForegroundColor Green
    Write-Host "- Activation automatique Material Preview" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "SOLUTION PROBLÈME TEXTURES:" -ForegroundColor Yellow
    Write-Host "1. Installer v1.5.2 dans Blender" -ForegroundColor White
    Write-Host "2. Activer Advanced Texture System" -ForegroundColor White
    Write-Host "3. Définir Texture Base Path" -ForegroundColor White
    Write-Host "4. Générer un district OU" -ForegroundColor White
    Write-Host "5. Cliquer Forcer Textures Bâtiments" -ForegroundColor White
    Write-Host "6. Vérifier en Material Preview" -ForegroundColor White
    
    Write-Host ""
    Write-Host "IMPORTANT:" -ForegroundColor Red
    Write-Host "- Le bouton FORCE TEXTURES applique les textures" -ForegroundColor Yellow
    Write-Host "- aux bâtiments déjà créés dans la scène" -ForegroundColor Yellow
    Write-Host "- Remplace tous les matériaux existants" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Appuyez sur une touche..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
