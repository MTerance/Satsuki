$files = Get-ChildItem "C:\Users\sshom\source\repos\Satsuki\Satsuki" -Recurse -Include "*.cs" -Exclude "*AssemblyInfo.cs","*AssemblyAttributes.cs"

$count = 0

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        if ($null -eq $content) { continue }
        
        $original = $content
        
        # Remplacer uniquement les caracteres accentues (pas les operateurs !)
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
        
        # Supprimer les emojis courants (liste exhaustive)
        $emojis = @('??','??','??','?','?','??','??','??','??','???','??','???','??','??','??','??','??','???','??','??','??','??','??','??','??','??','?','??','??','??','??','??','??','?','??','??','??','???','??','???','??','??','??','???','??','???','???','??','??','??','??','???','??','??','???','??','??','??','??','??','???','??','??','???','??','??','??','??','??','??','??','??','??')
        foreach ($emoji in $emojis) {
            $content = $content -replace [regex]::Escape($emoji), ''
        }
        
        if ($content -ne $original) {
            Set-Content $file.FullName $content -NoNewline -Encoding UTF8
            $count++
            Write-Host "Corrige: $($file.Name)"
        }
    }
    catch {
        Write-Host "Erreur sur $($file.Name): $_"
    }
}

Write-Host "Total: $count fichiers corriges"
