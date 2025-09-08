# SCRIPT POWERSHELL - CRÉATION ZIP ADDON TOKYO v1.4.0
# Crée un ZIP prêt pour installation dans Blender

param(
    [string]$Version = "1.4.0"
)

# Configuration
$SourceDir = "c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0"
$OutputDir = "c:\Users\sshom\Documents\assets\Tools"
$ZipName = "tokyo_city_generator_v$Version.zip"
$ZipPath = Join-Path $OutputDir $ZipName

Write-Host "🚀 CRÉATION ZIP ADDON TOKYO v$Version" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Yellow

# Vérifier que le dossier source existe
if (-not (Test-Path $SourceDir)) {
    Write-Host "❌ ERREUR: Dossier source non trouvé: $SourceDir" -ForegroundColor Red
    exit 1
}

# Créer le dossier de sortie si nécessaire
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    Write-Host "📁 Dossier de sortie créé: $OutputDir" -ForegroundColor Green
}

# Supprimer l'ancien ZIP s'il existe
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
    Write-Host "🗑️ Ancien ZIP supprimé" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📦 CRÉATION DU ZIP..." -ForegroundColor Cyan
Write-Host "📁 Source: $SourceDir" -ForegroundColor Gray
Write-Host "🎯 Destination: $ZipPath" -ForegroundColor Gray

# Fichiers essentiels à inclure dans le ZIP
$EssentialFiles = @(
    "__init__.py",
    "texture_system.py", 
    "setup_textures.py",
    "README.md"
)

# Vérifier que les fichiers essentiels existent
Write-Host ""
Write-Host "🔍 VÉRIFICATION FICHIERS ESSENTIELS:" -ForegroundColor Cyan

$AllFilesExist = $true
foreach ($File in $EssentialFiles) {
    $FilePath = Join-Path $SourceDir $File
    if (Test-Path $FilePath) {
        $FileSize = (Get-Item $FilePath).Length
        Write-Host "  ✅ $File ($([math]::Round($FileSize/1KB, 2)) KB)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $File - MANQUANT" -ForegroundColor Red
        $AllFilesExist = $false
    }
}

if (-not $AllFilesExist) {
    Write-Host ""
    Write-Host "❌ ERREUR: Fichiers essentiels manquants!" -ForegroundColor Red
    exit 1
}

# Créer le ZIP avec PowerShell
try {
    Write-Host ""
    Write-Host "📦 COMPRESSION EN COURS..." -ForegroundColor Cyan
    
    # Utiliser Compress-Archive (PowerShell 5.0+)
    $FilesToZip = @()
    
    foreach ($File in $EssentialFiles) {
        $FilePath = Join-Path $SourceDir $File
        if (Test-Path $FilePath) {
            $FilesToZip += $FilePath
        }
    }
    
    # Créer l'archive
    Compress-Archive -Path $FilesToZip -DestinationPath $ZipPath -Force
    
    Write-Host "✅ ZIP créé avec succès!" -ForegroundColor Green
    
} catch {
    Write-Host "❌ ERREUR lors de la création du ZIP: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Vérifier le ZIP créé
if (Test-Path $ZipPath) {
    $ZipSize = (Get-Item $ZipPath).Length
    Write-Host ""
    Write-Host "📊 INFORMATIONS ZIP:" -ForegroundColor Cyan
    Write-Host "  📁 Fichier: $ZipPath" -ForegroundColor Gray
    Write-Host "  📦 Taille: $([math]::Round($ZipSize/1KB, 2)) KB" -ForegroundColor Gray
    
    # Lister le contenu du ZIP
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $Archive = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
        
        Write-Host "  📋 Contenu:" -ForegroundColor Gray
        foreach ($Entry in $Archive.Entries) {
            $EntrySize = [math]::Round($Entry.Length/1KB, 2)
            Write-Host "    📄 $($Entry.Name) ($EntrySize KB)" -ForegroundColor White
        }
        
        $Archive.Dispose()
        
    } catch {
        Write-Host "  ⚠️ Impossible de lister le contenu du ZIP" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ ERREUR: ZIP non créé!" -ForegroundColor Red
    exit 1
}

# Instructions d'installation
Write-Host ""
Write-Host "🎯 INSTRUCTIONS INSTALLATION BLENDER:" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Yellow
Write-Host "1. 🖥️ Ouvrez Blender" -ForegroundColor White
Write-Host "2. ⚙️ Edit > Preferences > Add-ons" -ForegroundColor White
Write-Host "3. 📦 Cliquez 'Install...'" -ForegroundColor White
Write-Host "4. 📁 Sélectionnez le fichier:" -ForegroundColor White
Write-Host "   $ZipPath" -ForegroundColor Cyan
Write-Host "5. ✅ Cliquez 'Install Add-on'" -ForegroundColor White
Write-Host "6. 🔍 Cherchez 'Tokyo' dans la liste" -ForegroundColor White
Write-Host "7. ✅ Activez 'Tokyo City Generator $Version'" -ForegroundColor White
Write-Host "8. 📐 Vue 3D > N > Onglet Tokyo" -ForegroundColor White

# Créer un fichier d'instructions
$InstructionsPath = Join-Path $OutputDir "INSTALLATION_ZIP_$Version.txt"
$Instructions = @"
# INSTALLATION TOKYO CITY GENERATOR v$Version VIA ZIP

## 📦 FICHIER ZIP CRÉÉ:
$ZipPath

## 🚀 ÉTAPES D'INSTALLATION:

1. 🖥️ Ouvrez Blender
2. ⚙️ Edit > Preferences > Add-ons  
3. 📦 Cliquez 'Install...'
4. 📁 Naviguez vers:
   $ZipPath
5. 📂 Sélectionnez le fichier ZIP
6. ✅ Cliquez 'Install Add-on'
7. 🔍 Dans la liste, cherchez 'Tokyo'
8. ✅ Cochez 'Tokyo City Generator $Version TEXTURE SYSTEM'
9. 💾 Sauvegardez les préférences
10. 📐 Vue 3D > Sidebar (N) > Onglet 'Tokyo'

## 🎨 FONCTIONNALITÉS v${Version}:
- ✅ Système de textures intelligent
- ✅ Sélection automatique selon dimensions bâtiments
- ✅ Interface 'Advanced Textures' + 'Texture Path'
- ✅ 25 dossiers de textures organisés
- ✅ Génération automatique de villes réalistes

## 🔧 SI PROBLÈME:
- Vérifiez que Blender est en version 4.0+
- Redémarrez Blender après installation
- Utilisez Install from Disk au lieu de dossier

Date: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')
"@

Set-Content -Path $InstructionsPath -Value $Instructions -Encoding UTF8
Write-Host ""
Write-Host "📝 Instructions sauvées: $InstructionsPath" -ForegroundColor Green

# Ouvrir le dossier de destination
Write-Host ""
Write-Host "📂 Ouverture du dossier..." -ForegroundColor Cyan
Start-Process "explorer.exe" -ArgumentList $OutputDir

Write-Host ""
Write-Host "🎉 SCRIPT TERMINÉ AVEC SUCCÈS!" -ForegroundColor Green
Write-Host "📦 ZIP prêt pour installation: $ZipName" -ForegroundColor Yellow
Write-Host "🚀 Utilisez ce ZIP dans Blender > Preferences > Add-ons > Install" -ForegroundColor Cyan
