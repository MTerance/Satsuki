# Script PowerShell pour packager l'addon City Block Generator
# Supprime l'ancien ZIP et cree un nouveau package

Write-Host "=== PACKAGING CITY BLOCK GENERATOR ADDON ===" -ForegroundColor Cyan
Write-Host ""

# Configuration - MISE À JOUR pour nouveau nom de dossier
$ZipName = "city_block_generator.zip"
$AddonDir = "city_block_generator"
$InitFile = "$AddonDir\__init__.py"

# Verifier si le dossier de l'addon existe
if (-Not (Test-Path $AddonDir)) {
    Write-Host "ERREUR: Le dossier '$AddonDir' n'existe pas!" -ForegroundColor Red
    Write-Host "   Assurez-vous d'etre dans le bon repertoire." -ForegroundColor Yellow
    exit 1
}

Write-Host "Dossier source trouve: $AddonDir" -ForegroundColor Green

# Lire la version depuis __init__.py
$AddonVersion = "version inconnue"
if (Test-Path $InitFile) {
    try {
        $InitContent = Get-Content $InitFile -Raw
        if ($InitContent -match '"version":\s*\((\d+),\s*(\d+),\s*(\d+)\)') {
            $AddonVersion = "$($matches[1]).$($matches[2]).$($matches[3])"
            Write-Host "Version detectee: $AddonVersion" -ForegroundColor Green
        }
        else {
            Write-Host "AVERTISSEMENT: Version non trouvee dans __init__.py" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "AVERTISSEMENT: Erreur lecture version: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}
else {
    Write-Host "AVERTISSEMENT: Fichier __init__.py non trouve" -ForegroundColor Yellow
}

# Supprimer l'ancien fichier ZIP s'il existe
if (Test-Path $ZipName) {
    Write-Host "Suppression de l'ancien fichier: $ZipName" -ForegroundColor Yellow
    try {
        Remove-Item $ZipName -Force
        Write-Host "   Ancien ZIP supprime avec succes" -ForegroundColor Green
    }
    catch {
        Write-Host "   ERREUR lors de la suppression: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "Aucun ancien ZIP a supprimer" -ForegroundColor Blue
}

# Creer le nouveau fichier ZIP
Write-Host ""
Write-Host "Creation du nouveau package..." -ForegroundColor Cyan
Write-Host "   Source: $AddonDir\" -ForegroundColor Gray
Write-Host "   Destination: $ZipName" -ForegroundColor Gray

try {
    # Utiliser Compress-Archive pour creer le ZIP
    $CompressParams = @{
        Path = $AddonDir
        DestinationPath = $ZipName
        CompressionLevel = "Optimal"
        Force = $true
    }
    
    Compress-Archive @CompressParams
    
    Write-Host ""
    Write-Host "SUCCES! Package cree: $ZipName" -ForegroundColor Green
    
    # Afficher les informations du fichier
    if (Test-Path $ZipName) {
        $FileInfo = Get-Item $ZipName
        $FileSizeMB = [math]::Round($FileInfo.Length / 1MB, 2)
        Write-Host "   Taille du fichier: $FileSizeMB MB" -ForegroundColor Gray
        Write-Host "   Cree le: $($FileInfo.CreationTime)" -ForegroundColor Gray
        
        Write-Host ""
        Write-Host "PRET POUR L'INSTALLATION:" -ForegroundColor Green
        Write-Host "   1. Ouvrez Blender" -ForegroundColor White
        Write-Host "   2. Edit > Preferences > Add-ons" -ForegroundColor White
        Write-Host "   3. Install > Selectionnez $ZipName" -ForegroundColor White
        Write-Host "   4. Activez 'City Block Generator'" -ForegroundColor White
        Write-Host "   5. Version: $AddonVersion" -ForegroundColor Yellow
    }
}
catch {
    Write-Host ""
    Write-Host "ERREUR lors de la creation du package!" -ForegroundColor Red
    Write-Host "   Details: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== PACKAGING TERMINE ===" -ForegroundColor Cyan
