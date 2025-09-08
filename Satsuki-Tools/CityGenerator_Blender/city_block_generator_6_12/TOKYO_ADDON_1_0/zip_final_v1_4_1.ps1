# Script PowerShell FINAL - ZIP Tokyo v1.4.1 avec diagnostic intégré

$SourceDir = "c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0"
$OutputDir = "c:\Users\sshom\Documents\assets\Tools"
$TempDir = Join-Path $OutputDir "temp_tokyo_v1_4_1"
$AddonFolderName = "tokyo_city_generator"
$ZipName = "tokyo_city_generator_v1_4_1_diagnostic.zip"
$ZipPath = Join-Path $OutputDir $ZipName

Write-Host "CREATION ZIP FINAL - Tokyo v1.4.1 + Diagnostic Intégré" -ForegroundColor Green

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

Write-Host "Creation structure: $AddonFolderName/" -ForegroundColor Cyan

# Fichiers ESSENTIELS (diagnostic intégré dans __init__.py)
$CoreFiles = @(
    "__init__.py",
    "texture_system.py", 
    "setup_textures.py"
)

Write-Host "Copie fichiers core..."
$FilesOK = 0
foreach ($File in $CoreFiles) {
    $SourceFile = Join-Path $SourceDir $File
    $DestFile = Join-Path $AddonTempPath $File
    
    if (Test-Path $SourceFile) {
        Copy-Item $SourceFile $DestFile
        $FileSize = (Get-Item $SourceFile).Length
        Write-Host "  ✅ $File ($FileSize bytes)" -ForegroundColor Green
        $FilesOK++
    } else {
        Write-Host "  ❌ MANQUANT: $File" -ForegroundColor Red
    }
}

if ($FilesOK -eq 0) {
    Write-Host "Aucun fichier copié!" -ForegroundColor Red
    exit 1
}

# Créer README final
$ReadmeContent = @"
# TOKYO CITY GENERATOR v1.4.1 - DIAGNOSTIC INTÉGRÉ

## 🆕 NOUVEAUTÉS v1.4.1:
- ✅ Diagnostic automatique intégré dans l'interface
- ✅ Test visuel des textures directement dans Blender  
- ✅ Boutons de dépannage dans le panneau Tokyo
- ✅ Pas besoin de scripts externes

## 📦 INSTALLATION:
1. Blender > Edit > Preferences > Add-ons
2. Install > Sélectionner ce ZIP
3. Activer "Tokyo City Generator 1.4.1"
4. Vue 3D > N > Onglet Tokyo

## 🔧 SI TEXTURES NE MARCHENT PAS:
1. ✅ Cocher "Advanced Textures" 
2. 🔍 Cliquer "Diagnostic Textures" (nouveau bouton!)
3. 🧪 Cliquer "Test Visual" pour vérifier
4. Suivre les recommandations affichées

## 💡 UTILISATION:
- Interface complète dans l'onglet Tokyo
- Diagnostic automatique des problèmes
- Test visuel avec cubes de démonstration
- Messages d'aide directement dans Blender

Tout est maintenant intégré dans l'addon!
"@

$ReadmePath = Join-Path $AddonTempPath "README.txt"
Set-Content -Path $ReadmePath -Value $ReadmeContent -Encoding UTF8
Write-Host "  📝 README.txt créé" -ForegroundColor Cyan

Write-Host ""
Write-Host "Creation ZIP final..."

try {
    Compress-Archive -Path (Join-Path $TempDir "*") -DestinationPath $ZipPath -Force
    
    Write-Host "ZIP FINAL créé avec succès!" -ForegroundColor Green
    
    $ZipSize = (Get-Item $ZipPath).Length
    Write-Host "Taille: $ZipSize bytes" -ForegroundColor Gray
    Write-Host "Emplacement: $ZipPath" -ForegroundColor Cyan
    
} catch {
    Write-Host "Erreur: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Vérifier contenu
Write-Host ""
Write-Host "Contenu ZIP FINAL:" -ForegroundColor Yellow

try {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $Archive = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
    
    foreach ($Entry in $Archive.Entries) {
        Write-Host "  📄 $($Entry.FullName)" -ForegroundColor White
    }
    
    $Archive.Dispose()
    
} catch {
    Write-Host "Impossible de lister le contenu" -ForegroundColor Yellow
}

# Nettoyer
Remove-Item $TempDir -Recurse -Force

Write-Host ""
Write-Host "🎉 TOKYO v1.4.1 - DIAGNOSTIC INTÉGRÉ!" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Yellow
Write-Host "✅ Diagnostic automatique dans l'interface"
Write-Host "✅ Test visuel intégré"  
Write-Host "✅ Boutons dépannage dans le panneau"
Write-Host "✅ Messages d'aide dans Blender"
Write-Host ""
Write-Host "🚀 PLUS BESOIN DE SCRIPTS EXTERNES!"
Write-Host "Tout est dans le addon maintenant."
Write-Host ""
Write-Host "ZIP PRÊT: $ZipPath" -ForegroundColor Cyan

# Ouvrir dossier
Start-Process "explorer.exe" -ArgumentList $OutputDir
