$files = Get-ChildItem "C:\Users\sshom\source\repos\Satsuki\Satsuki" -Recurse -Include "*.cs" -Exclude "*AssemblyInfo.cs","*AssemblyAttributes.cs"

$replacements = @{
    'à' = 'a'
    'â' = 'a'
    'é' = 'e'
    'è' = 'e'
    'ê' = 'e'
    'î' = 'i'
    'ô' = 'o'
    'ù' = 'u'
    'û' = 'u'
    'ç' = 'c'
}

# Liste d'emojis a supprimer (remplaces par rien)
$emojis = @(
    '??', '??', '??', '?', '?', '??', '??', '??', '??', 
    '???', '??', '???', '??', '??', '??', '??', '??', '???',
    '??', '??', '??', '??', '??', '??', '??', '??', '?'
)

$count = 0
foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $original = $content
        
        # Remplacer les accents
        foreach ($key in $replacements.Keys) {
            $content = $content -replace $key, $replacements[$key]
        }
        
        # Supprimer les emojis
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
