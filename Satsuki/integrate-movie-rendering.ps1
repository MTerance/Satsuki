# Script pour intégrer Movie Rendering dans DecorManagerTool
# Date : 22 novembre 2025

$file = "C:\Users\sshom\source\repos\Satsuki\Satsuki\addons\decor_manager\DecorManagerTool.cs"

Write-Host "Integration de Movie Rendering dans DecorManagerTool..." -ForegroundColor Cyan

# Lire le fichier
$content = Get-Content $file -Raw

# Vérifier si déjà intégré
if ($content -match "CreateMovieRenderingSection\(\)")
{
    Write-Host "Movie Rendering deja integre!" -ForegroundColor Yellow
    exit
}

# Trouver et remplacer la section
$pattern = "CreateSpawnPointsSection\(\);\s+AddSeparator\(\);\s+_titleCameraPanel"
$replacement = @"
CreateSpawnPointsSection();
		
		AddSeparator();
		
		CreateMovieRenderingSection();
		
		AddSeparator();

		_titleCameraPanel
"@

if ($content -match $pattern)
{
    $content = $content -replace $pattern, $replacement
    
    # Sauvegarder
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($file, $content, $utf8NoBom)
    
    Write-Host "Integration reussie!" -ForegroundColor Green
    Write-Host "Fichier modifie: $file" -ForegroundColor Green
}
else
{
    Write-Host "Pattern non trouve - integration manuelle requise" -ForegroundColor Red
    Write-Host "Voir: addons/decor_manager/INTEGRATION_INSTRUCTIONS.md" -ForegroundColor Yellow
}
