# Script pour mettre à jour les références de Movie à Menu Rendering
# Date : 22 novembre 2025

$file = "C:\Users\sshom\source\repos\Satsuki\Satsuki\addons\decor_manager\DecorManagerTool.cs"

Write-Host "Mise a jour des references Movie -> Menu Rendering..." -ForegroundColor Cyan

# Lire le fichier
$content = Get-Content $file -Raw

# Remplacements
$content = $content -replace '_isMovieRenderingMode', '_isMenuRenderingMode'
$content = $content -replace 'HandleMovieRenderingInput', 'HandleMenuRenderingInput'

# Sauvegarder
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($file, $content, $utf8NoBom)

Write-Host "Mise a jour reussie!" -ForegroundColor Green
Write-Host "Fichier modifie: $file" -ForegroundColor Green
