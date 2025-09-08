# Script PowerShell simple pour créer tokyo_city_generator_v1_5_1_fixed.zip

Write-Host "CREATION TOKYO CITY GENERATOR v1.5.1 FIXED" -ForegroundColor Green

$projectRoot = $PSScriptRoot
$addonSource = Join-Path $projectRoot "TOKYO_ADDON_1_0"
$zipName = "tokyo_city_generator_v1_5_1_fixed.zip"
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

# Créer ZIP
try {
    Write-Host "Création ZIP..." -ForegroundColor Yellow
    
    $tempDir = Join-Path $env:TEMP "tokyo_fixed"
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
    Write-Host "CORRECTIONS v1.5.1:" -ForegroundColor Magenta
    Write-Host "- Import système de textures sécurisé" -ForegroundColor Green
    Write-Host "- Protection contre erreurs None" -ForegroundColor Green
    Write-Host "- Diagnostic amélioré" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "INSTALLER DANS BLENDER:" -ForegroundColor Yellow
    Write-Host "1. Edit > Preferences > Add-ons" -ForegroundColor White
    Write-Host "2. Install > Sélectionner $zipName" -ForegroundColor White
    Write-Host "3. Activer Tokyo City Generator 1.5.1" -ForegroundColor White
    Write-Host "4. Tester avec bouton Diagnostic" -ForegroundColor White
}

Write-Host ""
Write-Host "Appuyez sur une touche..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
