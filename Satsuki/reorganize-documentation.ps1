# Script de réorganisation de la documentation
# Date : 22 novembre 2025

Write-Host "?? Réorganisation de la documentation..." -ForegroundColor Cyan
Write-Host ""

$baseDir = "C:\Users\sshom\source\repos\Satsuki\Satsuki"
$docDir = Join-Path $baseDir "Documentation"

# Créer la structure de dossiers
$folders = @(
    "Documentation\01_Architecture",
    "Documentation\02_Features",
    "Documentation\03_Tools",
    "Documentation\04_Fixes",
    "Documentation\05_Systems",
    "Documentation\06_Guides",
    "Documentation\07_Reports",
    "Documentation\Archive"
)

Write-Host "?? Création de la structure de dossiers..." -ForegroundColor Yellow

foreach ($folder in $folders) {
    $fullPath = Join-Path $baseDir $folder
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "  ? Créé: $folder" -ForegroundColor Green
    } else {
        Write-Host "  ??  Existe: $folder" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "?? Déplacement des fichiers..." -ForegroundColor Yellow

# Définir les règles de déplacement
$moveRules = @{
    # Architecture
    "01_Architecture" = @(
        "MainGameScene_Complete_Architecture.md",
        "ServerArchitecture.md",
        "ILocation_Interface.md",
        "GETGAMESTATE_SYSTEM.md"
    )
    
    # Features
    "02_Features" = @(
        "DecorManager_SpawnPoints_Feature.md",
        "DecorManager_MenuRendering_Guide.md",
        "Camera_Context_System.md",
        "Credits_AutoLoad.md",
        "CREDITS_ISCENE_IMPLEMENTATION.md",
        "CREDITS_SCENARIO.md"
    )
    
    # Tools
    "03_Tools" = @(
        "DecorManagerTool_Guide.md",
        "DecorLoader_Guide.md",
        "DecorLoader_Summary.md",
        "DecorManagerTool_Summary.md",
        "LocationManager.md"
    )
    
    # Fixes
    "04_Fixes" = @(
        "DecorManager_Plugin_Loading_Fix.md",
        "DecorManager_Final_Solution.md",
        "Application_Close_Fix.md",
        "SplashScreen_Fade_Fix.md",
        "Title_Menu_Display_Fix.md",
        "Camera_System_Improvement.md",
        "Title_Camera_Activation.md",
        "Unicode_Fix_Complete_Report.md"
    )
    
    # Systems
    "05_Systems" = @(
        "CLIENT_TYPE_AUTHENTICATION.md",
        "CryptageSystem.md",
        "LocationManager_Integration.md",
        "LocationManager_Resume.md"
    )
    
    # Guides
    "06_Guides" = @(
        "MainMenu_Complete_Implementation.md",
        "Credits_Title_Navigation.md",
        "DecorLoader_MainGameScene_Example.md"
    )
    
    # Reports
    "07_Reports" = @(
        "Cleanup_Obsolete_Docs_Report.md",
        "Cleanup_Scripts_Report.md",
        "Documentation_Cleanup_Report.md"
    )
    
    # Archive (obsolètes)
    "Archive" = @(
        "DecorManager_Fix.md",
        "DecorManager_MovieRendering_Guide.md",
        "DecorManager_MovieRendering_Summary.md",
        "DecorManager_Path_Fix.md",
        "DecorManager_SpawnPoints_Summary.md",
        "DecorManager_Test_Guide.md",
        "Fix-Unicode-Script.md",
        "Restaurant_Fix_Summary.md",
        "Restaurant_Setup_Guide.md",
        "Restaurant_Title_Integration.md",
        "SplashScreen_Debug_Guide.md",
        "SubViewport_Fix.md",
        "Title_LobbyEx_Integration.md"
    )
}

$movedCount = 0
$skippedCount = 0

foreach ($folderName in $moveRules.Keys) {
    $targetFolder = Join-Path $docDir $folderName
    $files = $moveRules[$folderName]
    
    foreach ($file in $files) {
        $sourcePath = Join-Path $docDir $file
        $destPath = Join-Path $targetFolder $file
        
        if (Test-Path $sourcePath) {
            try {
                Move-Item -Path $sourcePath -Destination $destPath -Force
                Write-Host "  ? Déplacé: $file ? $folderName" -ForegroundColor Green
                $movedCount++
            }
            catch {
                Write-Host "  ? Erreur: $file - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        else {
            Write-Host "  ??  Absent: $file" -ForegroundColor Yellow
            $skippedCount++
        }
    }
}

Write-Host ""
Write-Host "?? Résumé:" -ForegroundColor Cyan
Write-Host "  - Fichiers déplacés: $movedCount" -ForegroundColor Green
Write-Host "  - Fichiers absents: $skippedCount" -ForegroundColor Yellow
Write-Host "  - Dossiers créés: $($folders.Count)" -ForegroundColor White
Write-Host ""
Write-Host "? Réorganisation terminée !" -ForegroundColor Green
