# Script PowerShell pour corriger et créer tokyo_city_generator_v1_5_1_fixed.zip
# Version 1.5.1 avec corrections d'import du système de textures

Write-Host "CORRECTION TOKYO CITY GENERATOR v1.5.1 - TEXTURE SYSTEM FIXED" -ForegroundColor Green
Write-Host "================================================================="

$projectRoot = $PSScriptRoot
$addonSource = Join-Path $projectRoot "TOKYO_ADDON_1_0"
$outputDir = $projectRoot
$zipName = "tokyo_city_generator_v1_5_1_fixed.zip"
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

# Vérifier les fichiers critiques et leurs tailles
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
        
        # Vérifications spécifiques
        if ($file -eq "__init__.py") {
            $content = Get-Content $filePath -Raw
            if ($content -match "tokyo_texture_system = None") {
                Write-Host "  ✓ Protection None ajoutée" -ForegroundColor Green
            }
            if ($content -match "version.*1.*5.*1") {
                Write-Host "  ✓ Version 1.5.1 détectée" -ForegroundColor Green
            }
        }
        
        if ($file -eq "texture_system.py") {
            $content = Get-Content $filePath -Raw
            if ($content -match "tokyo_texture_system = TokyoTextureSystem") {
                Write-Host "  ✓ Instance globale présente" -ForegroundColor Green
            }
        }
    } else {
        Write-Error "Fichier manquant: $file"
        exit 1
    }
}

# Créer le ZIP avec la structure correcte pour Blender
try {
    Write-Host "Création du ZIP corrigé..." -ForegroundColor Yellow
    
    # Utiliser la compression PowerShell
    $tempDir = Join-Path $env:TEMP "tokyo_addon_fixed"
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
    
    Write-Host "ZIP corrigé créé avec succès!" -ForegroundColor Green
    
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
Write-Host "ADDON TOKYO v1.5.1 FIXED PRÊT!" -ForegroundColor Green
Write-Host "Fichier: $zipName" -ForegroundColor Green
Write-Host ""
Write-Host "CORRECTIONS v1.5.1:" -ForegroundColor Magenta
Write-Host "- Import du système de textures sécurisé" -ForegroundColor Green
Write-Host "- Protection contre tokyo_texture_system = None" -ForegroundColor Green
Write-Host "- Diagnostic approfondi ajouté" -ForegroundColor Green
Write-Host "- Gestion d'erreurs renforcée" -ForegroundColor Green
Write-Host "- Test d'initialisation du système" -ForegroundColor Green
Write-Host ""
Write-Host "INSTRUCTIONS TEST:" -ForegroundColor Yellow
Write-Host "1. Désinstaller ancienne version dans Blender" -ForegroundColor White
Write-Host "2. Install... > Sélectionnez $zipName" -ForegroundColor White
Write-Host "3. Activer Tokyo City Generator 1.5.1" -ForegroundColor White
Write-Host "4. Utiliser 'Diagnostic Textures' pour test" -ForegroundColor White

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
