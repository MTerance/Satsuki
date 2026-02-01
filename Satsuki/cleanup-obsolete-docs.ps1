# Script de nettoyage des documentations obsolètes
# Date : 22 novembre 2025

Write-Host "?? Nettoyage des documentations obsolètes..." -ForegroundColor Cyan
Write-Host ""

$baseDir = "C:\Users\sshom\source\repos\Satsuki\Satsuki"

# Liste des fichiers obsolètes à supprimer
$obsoleteFiles = @(
    # Movie Rendering (remplacé par Menu Rendering)
    "Documentation\DecorManager_MovieRendering_Guide.md",
    "Documentation\DecorManager_MovieRendering_Summary.md",
    "Tools\MovieRendering_QuickStart.md",
    
    # Fichiers temporaires de fix
    "ACTION-REQUISE-REDEMARRAGE.md",
    "APRES-REDEMARRAGE-CHECKLIST.md",
    "DECORMANAGER-MAINTENANT.md",
    "DECORMANAGER-RESOLU.md",
    
    # Scripts de fix temporaires
    "fix-decormanager-cache.ps1",
    "fix-decormanager-ultimate.ps1",
    "fix-unicode.ps1",
    "integrate-movie-rendering.ps1",
    "update-menu-rendering.ps1",
    "add-menu-surfaces.ps1",
    "add-menu-classes.ps1",
    "reset-decormanager.ps1",
    
    # Anciens guides de fix
    "Documentation\DecorManager_Fix.md",
    "Documentation\DecorManager_Path_Fix.md",
    "Documentation\Fix-Unicode-Script.md",
    
    # Doublons ou anciennes versions
    "Documentation\DecorManager_SpawnPoints_Summary.md",
    "Documentation\Restaurant_Fix_Summary.md",
    "Documentation\SplashScreen_Debug_Guide.md",
    "Documentation\SubViewport_Fix.md",
    "Documentation\Restaurant_Setup_Guide.md",
    "Documentation\Restaurant_Title_Integration.md",
    "Documentation\Title_LobbyEx_Integration.md",
    
    # Fichiers intégration temporaires
    "addons\decor_manager\INTEGRATION_INSTRUCTIONS.md",
    
    # Doublons dans Tools
    "Tools\DecorManagerTool.cs"
)

$deletedCount = 0
$notFoundCount = 0

foreach ($file in $obsoleteFiles) {
    $fullPath = Join-Path $baseDir $file
    
    if (Test-Path $fullPath) {
        try {
            Remove-Item $fullPath -Force
            Write-Host "? Supprimé: $file" -ForegroundColor Green
            $deletedCount++
        }
        catch {
            Write-Host "? Erreur suppression: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "??  Déjà absent: $file" -ForegroundColor Yellow
        $notFoundCount++
    }
}

Write-Host ""
Write-Host "?? Résumé:" -ForegroundColor Cyan
Write-Host "  - Fichiers supprimés: $deletedCount" -ForegroundColor Green
Write-Host "  - Fichiers déjà absents: $notFoundCount" -ForegroundColor Yellow
Write-Host "  - Total traité: $($obsoleteFiles.Count)" -ForegroundColor White
Write-Host ""
Write-Host "? Nettoyage terminé !" -ForegroundColor Green
