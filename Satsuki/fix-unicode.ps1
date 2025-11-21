# =====================================================
# Script de correction Unicode pour le projet Satsuki
# =====================================================
# 
# Description:
#   Supprime les caracteres accentues et emojis des fichiers C#
#   tout en preservant les operateurs (?, ??, etc.)
#
# Usage:
#   .\fix-unicode.ps1
#
# Derniere verification: Build reussi
# =====================================================

Write-Host "=== Correction Unicode pour Satsuki ===" -ForegroundColor Cyan
Write-Host ""

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$files = Get-ChildItem $projectPath -Recurse -Include "*.cs" -Exclude "*AssemblyInfo.cs","*AssemblyAttributes.cs"

Write-Host "Fichiers a analyser: $($files.Count)" -ForegroundColor Yellow
Write-Host ""

$count = 0

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        if ($null -eq $content) { continue }
        
        $original = $content
        
        # Remplacer uniquement les caracteres accentues
        $content = $content -replace 'à', 'a'
        $content = $content -replace 'â', 'a'
        $content = $content -replace 'ä', 'a'
        $content = $content -replace 'é', 'e'
        $content = $content -replace 'è', 'e'
        $content = $content -replace 'ê', 'e'
        $content = $content -replace 'ë', 'e'
        $content = $content -replace 'î', 'i'
        $content = $content -replace 'ï', 'i'
        $content = $content -replace 'ô', 'o'
        $content = $content -replace 'ö', 'o'
        $content = $content -replace 'ù', 'u'
        $content = $content -replace 'û', 'u'
        $content = $content -replace 'ü', 'u'
        $content = $content -replace 'ÿ', 'y'
        $content = $content -replace 'ç', 'c'
        
        # Supprimer les emojis courants
        $emojis = @('??','??','??','?','?','??','??','??','??','???','??','???','??','??','??','??','??','???','??','??','??','??','??','??','??','??','?')
        foreach ($emoji in $emojis) {
            $content = $content -replace [regex]::Escape($emoji), ''
        }
        
        if ($content -ne $original) {
            Set-Content $file.FullName $content -NoNewline -Encoding UTF8
            $count++
            Write-Host "  [OK] $($file.Name)" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "  [ERREUR] $($file.Name): $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Resultat ===" -ForegroundColor Cyan
Write-Host "Total: $count fichier(s) corrige(s)" -ForegroundColor $(if($count -eq 0){'Green'}else{'Yellow'})
Write-Host ""

if ($count -eq 0) {
    Write-Host "Aucune correction necessaire. Projet conforme!" -ForegroundColor Green
} else {
    Write-Host "Verification recommandee:" -ForegroundColor Yellow
    Write-Host "  dotnet build Satsuki.csproj" -ForegroundColor White
}
