# Script PowerShell pour packager l'addon City Block Generator CLEAN
# Version corrigée et fonctionnelle

Write-Host "=== PACKAGING CITY BLOCK GENERATOR CLEAN ===" -ForegroundColor Cyan
Write-Host ""

# Configuration
$ZipName = "city_block_generator_v6_13_8_CLEAN.zip"
$AddonDir = "city_block_generator_clean"

# Vérifier si le dossier existe
if (-Not (Test-Path $AddonDir)) {
    Write-Host "ERREUR: Le dossier '$AddonDir' n'existe pas!" -ForegroundColor Red
    exit 1
}

Write-Host "Dossier source: $AddonDir" -ForegroundColor Green

# Supprimer l'ancien ZIP s'il existe
if (Test-Path $ZipName) {
    Write-Host "Suppression de l'ancien fichier: $ZipName" -ForegroundColor Yellow
    Remove-Item $ZipName -Force
}

# Créer le nouveau fichier ZIP
Write-Host ""
Write-Host "Création du package CLEAN..." -ForegroundColor Cyan
Write-Host "   Source: $AddonDir\" -ForegroundColor Gray
Write-Host "   Destination: $ZipName" -ForegroundColor Gray

try {
    Compress-Archive -Path $AddonDir -DestinationPath $ZipName -CompressionLevel Optimal -Force
    
    Write-Host ""
    Write-Host "SUCCÈS! Package CLEAN créé: $ZipName" -ForegroundColor Green
    
    # Afficher les informations du fichier
    if (Test-Path $ZipName) {
        $FileInfo = Get-Item $ZipName
        $FileSizeMB = [math]::Round($FileInfo.Length / 1MB, 2)
        Write-Host "   Taille du fichier: $FileSizeMB MB" -ForegroundColor Gray
        Write-Host "   Créé le: $($FileInfo.CreationTime)" -ForegroundColor Gray
        
        Write-Host ""
        Write-Host "READY FOR BLENDER INSTALLATION:" -ForegroundColor Green
        Write-Host "   1. Ouvrez Blender" -ForegroundColor White
        Write-Host "   2. Edit > Preferences > Add-ons" -ForegroundColor White
        Write-Host "   3. Install > Sélectionnez $ZipName" -ForegroundColor White
        Write-Host "   4. Activez 'City Block Generator'" -ForegroundColor White
        Write-Host "   5. Version: 6.13.8 - VARIETY UPDATE CLEAN" -ForegroundColor Yellow
        
        Write-Host ""
        Write-Host "NOUVELLES FONCTIONNALITÉS:" -ForegroundColor Cyan
        Write-Host "   • 6x plus de variété visuelle" -ForegroundColor White
        Write-Host "   • 18 couleurs par zone" -ForegroundColor White
        Write-Host "   • 10 types de bâtiments" -ForegroundColor White
        Write-Host "   • Variations urbaines" -ForegroundColor White
        Write-Host "   • Interface simplifiée" -ForegroundColor White
    }
}
catch {
    Write-Host ""
    Write-Host "ERREUR lors de la création du package!" -ForegroundColor Red
    Write-Host "   Détails: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== PACKAGING CLEAN TERMINÉ ===" -ForegroundColor Cyan