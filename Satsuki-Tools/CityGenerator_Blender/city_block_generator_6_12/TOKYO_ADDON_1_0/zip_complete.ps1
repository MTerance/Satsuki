# Script PowerShell COMPLET - ZIP addon Tokyo v1.4.0 + Outils diagnostic

$SourceDir = "c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0"
$OutputDir = "c:\Users\sshom\Documents\assets\Tools"
$TempDir = Join-Path $OutputDir "temp_tokyo_complete"
$AddonFolderName = "tokyo_city_generator"
$ZipName = "tokyo_city_generator_v1_4_0_complete.zip"
$ZipPath = Join-Path $OutputDir $ZipName

Write-Host "CREATION ZIP COMPLET - Tokyo v1.4.0 + Diagnostic" -ForegroundColor Green

# Nettoyer
if (Test-Path $TempDir) {
    Remove-Item $TempDir -Recurse -Force
}
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

# Créer structure
$AddonTempPath = Join-Path $TempDir $AddonFolderName
New-Item -ItemType Directory -Path $AddonTempPath -Force

Write-Host "Creation structure complete: $AddonFolderName/" -ForegroundColor Cyan

# Fichiers ESSENTIELS addon
$CoreFiles = @(
    "__init__.py",
    "texture_system.py", 
    "setup_textures.py"
)

# Fichiers DIAGNOSTIC et AIDE
$DiagnosticFiles = @(
    "diagnostic_textures.py",
    "test_textures_simple.py",
    "GUIDE_RESOLUTION_TEXTURES.md"
)

Write-Host "Copie fichiers core addon..."
$FilesOK = 0
foreach ($File in $CoreFiles) {
    $SourceFile = Join-Path $SourceDir $File
    $DestFile = Join-Path $AddonTempPath $File
    
    if (Test-Path $SourceFile) {
        Copy-Item $SourceFile $DestFile
        $FileSize = (Get-Item $SourceFile).Length
        Write-Host "  CORE: $File ($FileSize bytes)" -ForegroundColor Green
        $FilesOK++
    } else {
        Write-Host "  MANQUANT: $File" -ForegroundColor Red
    }
}

Write-Host "Copie fichiers diagnostic..."
foreach ($File in $DiagnosticFiles) {
    $SourceFile = Join-Path $SourceDir $File
    $DestFile = Join-Path $AddonTempPath $File
    
    if (Test-Path $SourceFile) {
        Copy-Item $SourceFile $DestFile
        $FileSize = (Get-Item $SourceFile).Length
        Write-Host "  DIAG: $File ($FileSize bytes)" -ForegroundColor Yellow
        $FilesOK++
    } else {
        Write-Host "  MANQUANT: $File" -ForegroundColor Red
    }
}

# Créer README installation
$ReadmeContent = @"
# TOKYO CITY GENERATOR v1.4.0 - INSTALLATION & DIAGNOSTIC

## INSTALLATION:
1. Blender > Edit > Preferences > Add-ons
2. Install > Sélectionner ce ZIP
3. Activer "Tokyo City Generator 1.4.0"
4. Vue 3D > N > Onglet Tokyo

## SI TEXTURES NE MARCHENT PAS:
1. Cocher "Advanced Textures"
2. Dans Text Editor Blender:
   exec(open('diagnostic_textures.py').read())
3. Suivre les recommandations

## FICHIERS INCLUS:
- __init__.py: Addon principal
- texture_system.py: Système de textures intelligent  
- setup_textures.py: Configuration auto dossiers
- diagnostic_textures.py: Diagnostic problèmes
- test_textures_simple.py: Test visuel
- GUIDE_RESOLUTION_TEXTURES.md: Guide complet

## HELP:
Voir GUIDE_RESOLUTION_TEXTURES.md pour résoudre tous problèmes
"@

$ReadmePath = Join-Path $AddonTempPath "README_INSTALL.txt"
Set-Content -Path $ReadmePath -Value $ReadmeContent -Encoding UTF8
Write-Host "  README: README_INSTALL.txt créé" -ForegroundColor Cyan

Write-Host ""
Write-Host "Creation ZIP complet..."

try {
    Compress-Archive -Path (Join-Path $TempDir "*") -DestinationPath $ZipPath -Force
    
    Write-Host "ZIP COMPLET créé avec succès!" -ForegroundColor Green
    
    $ZipSize = (Get-Item $ZipPath).Length
    Write-Host "Taille: $ZipSize bytes" -ForegroundColor Gray
    Write-Host "Emplacement: $ZipPath" -ForegroundColor Cyan
    
} catch {
    Write-Host "Erreur: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Vérifier contenu
Write-Host ""
Write-Host "Contenu ZIP COMPLET:" -ForegroundColor Yellow

try {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $Archive = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
    
    foreach ($Entry in $Archive.Entries) {
        $Type = if ($Entry.Name.EndsWith(".py")) { "SCRIPT" } elseif ($Entry.Name.EndsWith(".md") -or $Entry.Name.EndsWith(".txt")) { "DOC" } else { "OTHER" }
        Write-Host "  [$Type] $($Entry.FullName)" -ForegroundColor White
    }
    
    $Archive.Dispose()
    
} catch {
    Write-Host "Impossible de lister le contenu" -ForegroundColor Yellow
}

# Nettoyer
Remove-Item $TempDir -Recurse -Force

Write-Host ""
Write-Host "INSTALLATION + DIAGNOSTIC:" -ForegroundColor Yellow
Write-Host "1. Installer le ZIP dans Blender"
Write-Host "2. Si problème textures: exec(open('diagnostic_textures.py').read())"
Write-Host "3. Voir README_INSTALL.txt dans l'addon"
Write-Host ""
Write-Host "ZIP COMPLET prêt: $ZipPath" -ForegroundColor Green

# Ouvrir dossier
Start-Process "explorer.exe" -ArgumentList $OutputDir
