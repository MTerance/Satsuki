# JP Building Generator - PowerShell Package Creator
param(
    [string]$Version = "0.1.4",
    [string]$OutputDir = ".",
    [switch]$IncludeDocs = $false
)

$AddonName = "jp_buildgen"
$ZipName = "${AddonName}_v${Version}.zip"
$SourceDir = $PSScriptRoot
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

# Liste des fichiers essentiels
$EssentialFiles = @(
    "__init__.py",
    "core.py", 
    "operators.py",
    "panels.py",
    "properties.py"
)

# Vérifier les fichiers essentiels
Write-Host "Checking essential files..." -ForegroundColor Gray
$AllFilesExist = $true
foreach ($file in $EssentialFiles) {
    $sourcePath = Join-Path $SourceDir $file
    if (Test-Path $sourcePath) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (not found)" -ForegroundColor Red
        $AllFilesExist = $false
    }
}

if (-not $AllFilesExist) {
    Write-Host ""
    Write-Host "ERROR: Missing essential files!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Préparer la liste des fichiers à compresser
$FilesToCompress = @()
foreach ($file in $EssentialFiles) {
    $FilesToCompress += $file
}

# Ajouter README si demandé
if ($IncludeDocs -and (Test-Path (Join-Path $SourceDir "README.md"))) {
    $FilesToCompress += "README.md"
    Write-Host "  ✓ README.md (included)" -ForegroundColor Green
}

# Ajouter textures si le dossier existe
if (Test-Path (Join-Path $SourceDir "textures")) {
    $FilesToCompress += "textures"
    Write-Host "  ✓ textures/ (included)" -ForegroundColor Green
}

# Supprimer l'ancien ZIP
if (Test-Path $OutputPath) {
    Write-Host "Removing existing package..." -ForegroundColor Gray
    Remove-Item $OutputPath -Force
}

# Créer le ZIP
Write-Host "Creating ZIP package..." -ForegroundColor Gray
try {
    Compress-Archive -Path $FilesToCompress -DestinationPath $OutputPath -Force
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
    Write-Host "3. Click Install button" -ForegroundColor Gray
    Write-Host "4. Select the $ZipName file" -ForegroundColor Gray
    Write-Host "5. Enable the JP Building Generator addon" -ForegroundColor Gray
} catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host " ERROR! Failed to create package" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to continue"