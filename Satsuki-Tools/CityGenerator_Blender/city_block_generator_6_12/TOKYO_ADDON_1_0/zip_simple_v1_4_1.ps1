# Script simple pour ZIP Tokyo v1.4.1

$SourceDir = "c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0"
$OutputDir = "c:\Users\sshom\Documents\assets\Tools"
$TempDir = Join-Path $OutputDir "temp_tokyo_simple"
$AddonFolderName = "tokyo_city_generator"
$ZipName = "tokyo_city_generator_v1_4_1_final.zip"
$ZipPath = Join-Path $OutputDir $ZipName

Write-Host "Creation ZIP Tokyo v1.4.1 FINAL"

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

# Fichiers essentiels
$Files = @(
    "__init__.py",
    "texture_system.py", 
    "setup_textures.py"
)

Write-Host "Copie des fichiers..."
$FilesOK = 0
foreach ($File in $Files) {
    $SourceFile = Join-Path $SourceDir $File
    $DestFile = Join-Path $AddonTempPath $File
    
    if (Test-Path $SourceFile) {
        Copy-Item $SourceFile $DestFile
        $FileSize = (Get-Item $SourceFile).Length
        Write-Host "OK: $File ($FileSize bytes)"
        $FilesOK++
    } else {
        Write-Host "MANQUANT: $File"
    }
}

if ($FilesOK -eq 0) {
    Write-Host "Aucun fichier copie!"
    exit 1
}

Write-Host "Creation du ZIP..."

try {
    Compress-Archive -Path (Join-Path $TempDir "*") -DestinationPath $ZipPath -Force
    
    Write-Host "ZIP cree avec succes!"
    
    $ZipSize = (Get-Item $ZipPath).Length
    Write-Host "Taille: $ZipSize bytes"
    Write-Host "Emplacement: $ZipPath"
    
} catch {
    Write-Host "Erreur: $($_.Exception.Message)"
    exit 1
}

# Nettoyer
Remove-Item $TempDir -Recurse -Force

Write-Host ""
Write-Host "TOKYO v1.4.1 FINAL READY!"
Write-Host "Diagnostic integre dans le addon"
Write-Host "Boutons dans le interface Tokyo"
Write-Host ""
Write-Host "ZIP pret: $ZipPath"

# Ouvrir dossier
Start-Process explorer.exe $OutputDir
