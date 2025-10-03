# DEPLOIEMENT ADDON V6.14.1 - CORRECTION DIAGONALES
# Script PowerShell pour deploiement rapide

Write-Host "=== DEPLOIEMENT ADDON V6.14.1 - CORRECTION DIAGONALES ===" -ForegroundColor Green
Write-Host "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host ""

# Chemins
$SourcePath = "..\1_ADDON_CLEAN"
$TargetPath = "C:\Users\sshom\Documents\assets\Tools\city_block_generator_6_14_1"
$BlenderPath = "C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\city_block_generator_6_14_1"

# Fichiers requis
$RequiredFiles = @("__init__.py", "generator.py", "operators.py", "ui.py")

Write-Host "=== VERIFICATION SOURCE ===" -ForegroundColor Cyan
Write-Host "Source: $SourcePath" -ForegroundColor Yellow

$TotalSize = 0
foreach ($File in $RequiredFiles) {
    $FilePath = Join-Path $SourcePath $File
    if (Test-Path $FilePath) {
        $Size = (Get-Item $FilePath).Length
        $TotalSize += $Size
        Write-Host "   OK $File`: $($Size.ToString('N0')) bytes" -ForegroundColor Green
    } else {
        Write-Host "   ERREUR $File`: MANQUANT!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Taille totale source: $($TotalSize.ToString('N0')) bytes" -ForegroundColor Yellow

# Verifier version
$InitPath = Join-Path $SourcePath "__init__.py"
$InitContent = Get-Content $InitPath -Raw
if ($InitContent -match '"version": \(6, 14, 1\)') {
    Write-Host "   OK Version 6.14.1 confirmee" -ForegroundColor Green
} else {
    Write-Host "   ATTENTION Version non confirmee" -ForegroundColor Yellow
}

# Verifier correction diagonales
$GenPath = Join-Path $SourcePath "generator.py"
$GenContent = Get-Content $GenPath -Raw
if ($GenContent -match 'if False:  # curve_intensity > 0\.7') {
    Write-Host "   OK Correction diagonales confirmee" -ForegroundColor Green
} else {
    Write-Host "   ERREUR Correction diagonales NON TROUVEE!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== DEPLOIEMENT DOUBLE ===" -ForegroundColor Cyan

# Deploiement 1: Assets
Write-Host "1. Deploiement vers assets..." -ForegroundColor Yellow
if (Test-Path $TargetPath) {
    Write-Host "Suppression ancien addon assets..." -ForegroundColor Yellow
    Remove-Item $TargetPath -Recurse -Force -ErrorAction SilentlyContinue
}

$TargetParent = Split-Path $TargetPath -Parent
if (!(Test-Path $TargetParent)) {
    New-Item -ItemType Directory -Path $TargetParent -Force | Out-Null
}

Copy-Item $SourcePath $TargetPath -Recurse -Force
Write-Host "   OK Copie vers: $TargetPath" -ForegroundColor Green

# Deploiement 2: Blender
Write-Host "2. Deploiement vers Blender..." -ForegroundColor Yellow
if (Test-Path $BlenderPath) {
    Write-Host "Suppression ancien addon Blender..." -ForegroundColor Yellow
    Remove-Item $BlenderPath -Recurse -Force -ErrorAction SilentlyContinue
}

$BlenderParent = Split-Path $BlenderPath -Parent
if (!(Test-Path $BlenderParent)) {
    New-Item -ItemType Directory -Path $BlenderParent -Force | Out-Null
}

Copy-Item $SourcePath $BlenderPath -Recurse -Force
Write-Host "   OK Copie vers: $BlenderPath" -ForegroundColor Green

Write-Host ""
Write-Host "=== VERIFICATION FINALE ===" -ForegroundColor Cyan

# Verifier assets
Write-Host "Verification assets..." -ForegroundColor Yellow
foreach ($File in $RequiredFiles) {
    $FilePath = Join-Path $TargetPath $File
    if (Test-Path $FilePath) {
        $Size = (Get-Item $FilePath).Length
        Write-Host "   OK $File`: $($Size.ToString('N0')) bytes" -ForegroundColor Green
    } else {
        Write-Host "   ERREUR $File`: ECHEC!" -ForegroundColor Red
        exit 1
    }
}

# Verifier Blender
Write-Host "Verification Blender..." -ForegroundColor Yellow
foreach ($File in $RequiredFiles) {
    $FilePath = Join-Path $BlenderPath $File
    if (Test-Path $FilePath) {
        $Size = (Get-Item $FilePath).Length
        Write-Host "   OK $File`: $($Size.ToString('N0')) bytes" -ForegroundColor Green
    } else {
        Write-Host "   ERREUR $File`: ECHEC!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "=== DEPLOIEMENT REUSSI ===" -ForegroundColor Green
Write-Host "Statistiques:" -ForegroundColor Yellow
Write-Host "   Version: 6.14.1" -ForegroundColor White
Write-Host "   Correction: Marques diagonales eliminees" -ForegroundColor White
Write-Host "   Assets: $TargetPath" -ForegroundColor White
Write-Host "   Blender: $BlenderPath" -ForegroundColor White
Write-Host "   Taille: $($TotalSize.ToString('N0')) bytes" -ForegroundColor White
Write-Host ""
Write-Host "=== INSTRUCTIONS BLENDER ===" -ForegroundColor Cyan
Write-Host "OPTION A - Auto (addon deja installe):" -ForegroundColor Yellow
Write-Host "   1. REDEMARRER Blender" -ForegroundColor White
Write-Host "   2. L'addon v6.14.1 est deja installe!" -ForegroundColor White
Write-Host "   3. Verifier version dans le panneau CityGen" -ForegroundColor White
Write-Host ""
Write-Host "OPTION B - Manuel (nouveau deploiement):" -ForegroundColor Yellow
Write-Host "   1. REDEMARRER Blender" -ForegroundColor White
Write-Host "   2. Edit > Preferences > Add-ons" -ForegroundColor White
Write-Host "   3. SUPPRIMER ancien addon si present" -ForegroundColor White
Write-Host "   4. Install > Selectionner dossier:" -ForegroundColor White
Write-Host "      $BlenderPath" -ForegroundColor Gray
Write-Host "   5. ACTIVER City Block Generator" -ForegroundColor White
Write-Host ""
Write-Host "=== TEST RECOMMANDE ===" -ForegroundColor Cyan
Write-Host "   Grille: 3x3" -ForegroundColor White
Write-Host "   Curve Intensity: 0.5" -ForegroundColor White
Write-Host "   Mode: Organique" -ForegroundColor White
Write-Host "   Attendu: Courbes SANS marques diagonales" -ForegroundColor White
Write-Host ""
Write-Host "DEPLOIEMENT V6.14.1 REUSSI !" -ForegroundColor Green
Write-Host "Correction diagonales appliquee" -ForegroundColor Green
Write-Host "Pret pour test courbes organiques" -ForegroundColor Green

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
