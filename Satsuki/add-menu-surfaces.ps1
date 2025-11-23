# Script pour ajouter MenuRenderSurfaces à DecorConfiguration
$file = "C:\Users\sshom\source\repos\Satsuki\Satsuki\addons\decor_manager\DecorManagerTool.cs"

Write-Host "Ajout de MenuRenderSurfaces a DecorConfiguration..." -ForegroundColor Cyan

# Lire le fichier
$content = Get-Content $file -Raw

# Rechercher et remplacer
$pattern = "public List<SpawnPointData> SpawnPoints \{ get; set; \}\s+public DateTime SavedAt"
$replacement = @"
public List<SpawnPointData> SpawnPoints { get; set; }
	public List<MenuRenderSurfaceData> MenuRenderSurfaces { get; set; }
	public DateTime SavedAt
"@

if ($content -match $pattern)
{
    $content = $content -replace $pattern, $replacement
    
    # Sauvegarder
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($file, $content, $utf8NoBom)
    
    Write-Host "Ajout reussi!" -ForegroundColor Green
}
else
{
    Write-Host "Pattern non trouve" -ForegroundColor Red
}
