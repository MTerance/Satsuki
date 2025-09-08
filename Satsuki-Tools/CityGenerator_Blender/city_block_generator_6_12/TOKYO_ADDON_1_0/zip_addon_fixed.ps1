# Script PowerShell CORRIGÉ pour créer ZIP addon Tokyo v1.4.0
# Crée la structure de dossier attendue par Blender

$SourceDir = "c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0"
$OutputDir = "c:\Users\sshom\Documents\assets\Tools"
$TempDir = Join-Path $OutputDir "temp_tokyo_addon"
$AddonFolderName = "tokyo_city_generator"
$ZipName = "tokyo_city_generator_v1_4_0_fixed.zip"
$ZipPath = Join-Path $OutputDir $ZipName

Write-Host "CORRECTION ZIP addon Tokyo v1.4.0 - Structure Blender" -ForegroundColor Green

# Nettoyer ancien temp et ZIP
if (Test-Path $TempDir) {
    Remove-Item $TempDir -Recurse -Force
}
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

# Créer dossier temporaire avec la bonne structure
$AddonTempPath = Join-Path $TempDir $AddonFolderName
New-Item -ItemType Directory -Path $AddonTempPath -Force

Write-Host "Creation structure: $AddonFolderName/" -ForegroundColor Cyan

# Fichiers à inclure
$Files = @(
    "__init__.py",
    "texture_system.py", 
    "setup_textures.py"
)

Write-Host "Copie des fichiers dans la structure addon..."

$FilesOK = 0
foreach ($File in $Files) {
    $SourceFile = Join-Path $SourceDir $File
    $DestFile = Join-Path $AddonTempPath $File
    
    if (Test-Path $SourceFile) {
        Copy-Item $SourceFile $DestFile
        $FileSize = (Get-Item $SourceFile).Length
        Write-Host "  OK: $AddonFolderName/$File ($FileSize bytes)" -ForegroundColor Green
        $FilesOK++
    } else {
        Write-Host "  MANQUANT: $File" -ForegroundColor Red
    }
}

if ($FilesOK -eq 0) {
    Write-Host "Aucun fichier copié!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Creation du ZIP avec structure Blender..."

try {
    # Créer le ZIP en incluant le dossier parent
    Compress-Archive -Path (Join-Path $TempDir "*") -DestinationPath $ZipPath -Force
    
    Write-Host "ZIP corrigé créé avec succès!" -ForegroundColor Green
    
    $ZipSize = (Get-Item $ZipPath).Length
    Write-Host "Taille: $ZipSize bytes" -ForegroundColor Gray
    Write-Host "Emplacement: $ZipPath" -ForegroundColor Cyan
    
} catch {
    Write-Host "Erreur: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Vérifier le contenu du ZIP
Write-Host ""
Write-Host "Verification structure ZIP..." -ForegroundColor Yellow

try {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $Archive = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
    
    Write-Host "Contenu du ZIP:"
    foreach ($Entry in $Archive.Entries) {
        Write-Host "  $($Entry.FullName)" -ForegroundColor White
    }
    
    $Archive.Dispose()
    
} catch {
    Write-Host "Impossible de lister le contenu" -ForegroundColor Yellow
}

# Nettoyer le dossier temporaire
Remove-Item $TempDir -Recurse -Force

Write-Host ""
Write-Host "INSTRUCTIONS INSTALLATION CORRIGÉES:" -ForegroundColor Yellow
Write-Host "1. Ouvrir Blender"
Write-Host "2. Edit > Preferences > Add-ons"
Write-Host "3. Install > Sélectionner le ZIP corrigé"
Write-Host "4. Activer Tokyo City Generator"
Write-Host ""
Write-Host "ZIP CORRIGÉ prêt: $ZipPath" -ForegroundColor Green
Write-Host "Structure: $AddonFolderName/__init__.py (comme attendu par Blender)" -ForegroundColor Cyan

# Ouvrir le dossier
Start-Process "explorer.exe" -ArgumentList $OutputDir
