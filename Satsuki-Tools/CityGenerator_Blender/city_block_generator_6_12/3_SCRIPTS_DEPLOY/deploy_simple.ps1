# Script de deploiement simple pour V6.14.1
# Sans emojis pour compatibilite PowerShell

param(
    [switch]$Force
)

Write-Host "=== DEPLOIEMENT ADDON V6.14.1 ===" -ForegroundColor Green
Write-Host "Date: $(Get-Date)" -ForegroundColor Yellow

# Chemins
$Source = "..\1_ADDON_CLEAN"
$Assets = "C:\Users\sshom\Documents\assets\Tools\city_block_generator_6_14_1" 
$Blender = "C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\city_block_generator_6_14_1"

# Verification source
Write-Host "Verification source..." -ForegroundColor Cyan
if (!(Test-Path $Source)) {
    Write-Host "ERREUR: Source introuvable: $Source" -ForegroundColor Red
    exit 1
}

$Files = @("__init__.py", "generator.py", "operators.py", "ui.py")
foreach ($File in $Files) {
    $Path = Join-Path $Source $File
    if (Test-Path $Path) {
        $Size = (Get-Item $Path).Length
        Write-Host "  OK $File ($($Size.ToString('N0')) bytes)" -ForegroundColor Green
    } else {
        Write-Host "  ERREUR $File manquant" -ForegroundColor Red
        exit 1
    }
}

# Deploiement Assets
Write-Host ""
Write-Host "Deploiement vers Assets..." -ForegroundColor Cyan
if (Test-Path $Assets) {
    if ($Force) {
        Remove-Item $Assets -Recurse -Force
        Write-Host "  Ancien dossier supprime" -ForegroundColor Yellow
    } else {
        Write-Host "  Dossier existe deja (utilisez -Force pour ecraser)" -ForegroundColor Yellow
        $Choice = Read-Host "Continuer quand meme? (o/n)"
        if ($Choice -ne "o") { exit 0 }
    }
}

try {
    $AssetsParent = Split-Path $Assets -Parent
    if (!(Test-Path $AssetsParent)) {
        New-Item -ItemType Directory -Path $AssetsParent -Force | Out-Null
    }
    Copy-Item $Source $Assets -Recurse -Force
    Write-Host "  SUCCESS: Copie vers Assets terminee" -ForegroundColor Green
} catch {
    Write-Host "  ERREUR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Deploiement Blender
Write-Host ""
Write-Host "Deploiement vers Blender..." -ForegroundColor Cyan
if (Test-Path $Blender) {
    Remove-Item $Blender -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  Ancien addon Blender supprime" -ForegroundColor Yellow
}

try {
    $BlenderParent = Split-Path $Blender -Parent
    if (!(Test-Path $BlenderParent)) {
        New-Item -ItemType Directory -Path $BlenderParent -Force | Out-Null
    }
    Copy-Item $Source $Blender -Recurse -Force
    Write-Host "  SUCCESS: Copie vers Blender terminee" -ForegroundColor Green
} catch {
    Write-Host "  ERREUR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Verification finale
Write-Host ""
Write-Host "Verification finale..." -ForegroundColor Cyan
$AllGood = $true

foreach ($File in $Files) {
    $AssetFile = Join-Path $Assets $File
    $BlenderFile = Join-Path $Blender $File
    
    if ((Test-Path $AssetFile) -and (Test-Path $BlenderFile)) {
        Write-Host "  OK $File present dans les deux destinations" -ForegroundColor Green
    } else {
        Write-Host "  ERREUR $File manquant quelque part" -ForegroundColor Red
        $AllGood = $false
    }
}

Write-Host ""
if ($AllGood) {
    Write-Host "=== DEPLOIEMENT REUSSI ===" -ForegroundColor Green
    Write-Host "Version: 6.14.1" -ForegroundColor White
    Write-Host "Assets: $Assets" -ForegroundColor White  
    Write-Host "Blender: $Blender" -ForegroundColor White
    Write-Host ""
    Write-Host "ETAPES SUIVANTES:" -ForegroundColor Yellow
    Write-Host "1. REDEMARRER Blender" -ForegroundColor White
    Write-Host "2. L'addon sera automatiquement disponible" -ForegroundColor White
    Write-Host "3. Ou installer manuellement depuis:" -ForegroundColor White
    Write-Host "   $Blender" -ForegroundColor Gray
    Write-Host ""
    Write-Host "TEST: Grille 3x3, Curve Intensity 0.5, Mode Organique" -ForegroundColor Cyan
} else {
    Write-Host "=== DEPLOIEMENT ECHOUE ===" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Appuyez sur Entree pour fermer..." -ForegroundColor Yellow
Read-Host
