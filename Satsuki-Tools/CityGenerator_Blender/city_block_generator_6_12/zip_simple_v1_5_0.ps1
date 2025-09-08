# Script PowerShell pour créer tokyo_city_generator_v1_5_0_roads.zip
# Version 1.5.0 avec système de routes et textures quadrants

Write-Host "CREATION TOKYO CITY GENERATOR v1.5.0 + ROADS" -ForegroundColor Green
Write-Host "=================================================="

$projectRoot = $PSScriptRoot
$addonSource = Join-Path $projectRoot "TOKYO_ADDON_1_0"
$outputDir = $projectRoot
$zipName = "tokyo_city_generator_v1_5_0_roads.zip"
$zipPath = Join-Path $outputDir $zipName

Write-Host "Répertoire source: $addonSource" -ForegroundColor Cyan
Write-Host "Fichier de sortie: $zipPath" -ForegroundColor Cyan

# Supprimer l'ancien ZIP s'il existe
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
    Write-Host "Ancien ZIP supprimé" -ForegroundColor Yellow
}

# Vérifier que le dossier source existe
if (-not (Test-Path $addonSource)) {
    Write-Error "Dossier source non trouvé: $addonSource"
    exit 1
}

# Vérifier les fichiers critiques
$criticalFiles = @(
    "__init__.py",
    "texture_system.py"
)

Write-Host "Vérification des fichiers critiques..." -ForegroundColor Yellow
foreach ($file in $criticalFiles) {
    $filePath = Join-Path $addonSource $file
    if (Test-Path $filePath) {
        $size = (Get-Item $filePath).Length
        Write-Host "OK: $file ($size bytes)" -ForegroundColor Green
    } else {
        Write-Error "Fichier manquant: $file"
        exit 1
    }
}

# Créer le ZIP avec la structure correcte pour Blender
try {
    Write-Host "Création du ZIP..." -ForegroundColor Yellow
    
    # Utiliser la compression PowerShell
    $tempDir = Join-Path $env:TEMP "tokyo_addon_temp"
    $addonDir = Join-Path $tempDir "tokyo_city_generator"
    
    # Nettoyer et créer le répertoire temporaire
    if (Test-Path $tempDir) {
        Remove-Item $tempDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $addonDir -Force | Out-Null
    
    # Copier tous les fichiers Python
    $filesToCopy = @("__init__.py", "texture_system.py")
    foreach ($file in $filesToCopy) {
        $sourcePath = Join-Path $addonSource $file
        $destPath = Join-Path $addonDir $file
        
        if (Test-Path $sourcePath) {
            Copy-Item $sourcePath $destPath -Force
            Write-Host "Copié: $file" -ForegroundColor Green
        }
    }
    
    # Créer le ZIP
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $zipPath)
    
    # Nettoyer
    Remove-Item $tempDir -Recurse -Force
    
    Write-Host "ZIP créé avec succès!" -ForegroundColor Green
    
} catch {
    Write-Error "Erreur lors de la création du ZIP: $_"
    exit 1
}

# Vérifications finales
if (Test-Path $zipPath) {
    $zipSize = (Get-Item $zipPath).Length
    Write-Host "Taille du ZIP: $zipSize bytes" -ForegroundColor Cyan
    
    # Test d'ouverture du ZIP
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
        $entries = $zip.Entries | Where-Object { $_.Name -like "*.py" }
        
        Write-Host "Contenu du ZIP:" -ForegroundColor Cyan
        foreach ($entry in $entries) {
            Write-Host "  $($entry.FullName) ($($entry.Length) bytes)" -ForegroundColor White
        }
        
        $zip.Dispose()
        Write-Host "ZIP valide et lisible" -ForegroundColor Green
        
    } catch {
        Write-Error "Erreur lors de la vérification du ZIP: $_"
    }
}

Write-Host ""
Write-Host "ADDON TOKYO v1.5.0 + ROADS PRÊT!" -ForegroundColor Green
Write-Host "Fichier: $zipName" -ForegroundColor Green
Write-Host ""
Write-Host "INSTRUCTIONS D'INSTALLATION:" -ForegroundColor Yellow
Write-Host "1. Ouvrez Blender" -ForegroundColor White
Write-Host "2. Edit > Preferences > Add-ons" -ForegroundColor White
Write-Host "3. Install... > Sélectionnez $zipName" -ForegroundColor White
Write-Host "4. Activez Tokyo City Generator 1.5.0" -ForegroundColor White
Write-Host "5. Vue 3D > Sidebar (N) > Onglet Tokyo" -ForegroundColor White
Write-Host ""
Write-Host "NOUVEAUTÉS v1.5.0:" -ForegroundColor Magenta
Write-Host "- Système de textures pour routes" -ForegroundColor Green
Write-Host "- Mapping UV par quadrants (4 zones)" -ForegroundColor Green
Write-Host "- Test visuel des routes et trottoirs" -ForegroundColor Green
Write-Host "- Support normal map et specular" -ForegroundColor Green
Write-Host "- Centre route / Bords / Trottoirs séparés" -ForegroundColor Green

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
