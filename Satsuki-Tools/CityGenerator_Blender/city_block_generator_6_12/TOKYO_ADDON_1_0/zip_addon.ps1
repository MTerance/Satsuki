# Script PowerShell pour créer ZIP addon Tokyo v1.4.0

$SourceDir = "c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0"
$OutputDir = "c:\Users\sshom\Documents\assets\Tools"
$ZipName = "tokyo_city_generator_v1_4_0.zip"
$ZipPath = Join-Path $OutputDir $ZipName

Write-Host "Creation ZIP addon Tokyo v1.4.0" -ForegroundColor Green

# Créer dossier output si nécessaire
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force
}

# Supprimer ancien ZIP
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

# Fichiers à inclure
$Files = @(
    "__init__.py",
    "texture_system.py", 
    "setup_textures.py"
)

Write-Host "Verification des fichiers..."

$FilesToZip = @()
foreach ($File in $Files) {
    $FilePath = Join-Path $SourceDir $File
    if (Test-Path $FilePath) {
        $FileSize = (Get-Item $FilePath).Length
        Write-Host "OK: $File ($FileSize bytes)" -ForegroundColor Green
        $FilesToZip += $FilePath
    } else {
        Write-Host "MANQUANT: $File" -ForegroundColor Red
    }
}

if ($FilesToZip.Count -eq 0) {
    Write-Host "Aucun fichier trouvé!" -ForegroundColor Red
    exit 1
}

Write-Host "Creation du ZIP..."

try {
    Compress-Archive -Path $FilesToZip -DestinationPath $ZipPath -Force
    Write-Host "ZIP créé avec succès!" -ForegroundColor Green
    
    $ZipSize = (Get-Item $ZipPath).Length
    Write-Host "Taille: $ZipSize bytes" -ForegroundColor Gray
    Write-Host "Emplacement: $ZipPath" -ForegroundColor Cyan
    
} catch {
    Write-Host "Erreur: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "INSTRUCTIONS INSTALLATION:" -ForegroundColor Yellow
Write-Host "1. Ouvrir Blender"
Write-Host "2. Edit > Preferences > Add-ons"
Write-Host "3. Install > Sélectionner le ZIP"
Write-Host "4. Activer Tokyo City Generator"
Write-Host ""
Write-Host "ZIP prêt: $ZipPath" -ForegroundColor Green

# Ouvrir le dossier
Start-Process "explorer.exe" -ArgumentList $OutputDir
