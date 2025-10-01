# JP Building Generator - PowerShell Package Creator
# Usage: .\package_addon.ps1

param(
    [string]$Version = "0.1.3",
    [string]$OutputDir = ".",
    [switch]$IncludeDocs = $false
)

$AddonName = "jp_buildgen"
$ZipName = "${AddonName}_v${Version}.zip"
$SourceDir = $PSScriptRoot
$TempDir = Join-Path $env:TEMP "${AddonName}_package"
$OutputPath = Join-Path $OutputDir $ZipName

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " JP Building Generator - Package Creator" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Source: $SourceDir"
Write-Host "  Version: $Version"
Write-Host "  Output: $OutputPath"
Write-Host "  Include docs: $IncludeDocs"
Write-Host ""

# Nettoyer et créer le répertoire temporaire
if (Test-Path $TempDir) {
    Write-Host "Cleaning temporary directory..." -ForegroundColor Gray
    Remove-Item $TempDir -Recurse -Force
}

Write-Host "Creating temporary structure..." -ForegroundColor Gray
$AddonTempDir = New-Item -Path (Join-Path $TempDir $AddonName) -ItemType Directory -Force

# Liste des fichiers essentiels
$EssentialFiles = @(
    "__init__.py",
    "core.py", 
    "operators.py",
    "panels.py",
    "properties.py"
)

# Copier les fichiers essentiels
Write-Host "Copying essential files..." -ForegroundColor Gray
foreach ($file in $EssentialFiles) {
    $sourcePath = Join-Path $SourceDir $file
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath $AddonTempDir -Force
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (not found)" -ForegroundColor Red
    }
}

# Copier le README si demandé ou s'il existe
$readmePath = Join-Path $SourceDir "README.md"
if ($IncludeDocs -or (Test-Path $readmePath)) {
    Write-Host "Copying documentation..." -ForegroundColor Gray
    Copy-Item $readmePath $AddonTempDir -Force -ErrorAction SilentlyContinue
    Write-Host "  ✓ README.md" -ForegroundColor Green
}

# Copier le dossier textures
$texturesPath = Join-Path $SourceDir "textures"
if (Test-Path $texturesPath) {
    Write-Host "Copying textures directory..." -ForegroundColor Gray
    Copy-Item $texturesPath $AddonTempDir -Recurse -Force
    Write-Host "  ✓ textures/" -ForegroundColor Green
} else {
    Write-Host "  ✗ textures/ (not found)" -ForegroundColor Yellow
}

# Supprimer l'ancien ZIP s'il existe
if (Test-Path $OutputPath) {
    Write-Host "Removing existing package..." -ForegroundColor Gray
    Remove-Item $OutputPath -Force
}

# Créer le ZIP
Write-Host "Creating ZIP package..." -ForegroundColor Gray
try {
    Compress-Archive -Path (Join-Path $TempDir $AddonName) -DestinationPath $OutputPath -Force
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host " SUCCESS! Package created successfully" -ForegroundColor Green  
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Package: $ZipName" -ForegroundColor White
    Write-Host "Location: $OutputPath" -ForegroundColor White
    Write-Host ""
    Write-Host "To install in Blender:" -ForegroundColor Yellow
    Write-Host "1. Open Blender" -ForegroundColor Gray
    Write-Host "2. Go to Edit -> Preferences -> Add-ons" -ForegroundColor Gray
    Write-Host "3. Click 'Install...' button" -ForegroundColor Gray
    Write-Host "4. Select the $ZipName file" -ForegroundColor Gray
    Write-Host "5. Enable the 'JP Building Generator' addon" -ForegroundColor Gray
} catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host " ERROR! Failed to create package" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    # Nettoyer le répertoire temporaire
    if (Test-Path $TempDir) {
        Remove-Item $TempDir -Recurse -Force
    }
}

Write-Host ""
Read-Host "Press Enter to continue"