$files = Get-ChildItem "C:\Users\sshom\source\repos\Satsuki\Satsuki" -Recurse -Include "*.cs" -Exclude "*AssemblyInfo.cs","*AssemblyAttributes.cs"

$count = 0
$totalChanges = 0

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        if ($null -eq $content) { continue }
        
        $original = $content
        
        # Remplacer TOUS les caracteres non-ASCII (sauf retours a la ligne)
        # Garder uniquement les caracteres ASCII imprimables (32-126) + \r\n\t
        $newContent = ""
        for ($i = 0; $i -lt $content.Length; $i++) {
            $char = $content[$i]
            $charCode = [int]$char
            
            # Garder: ASCII imprimable (32-126), \n (10), \r (13), \t (9)
            if (($charCode -ge 32 -and $charCode -le 126) -or $charCode -eq 10 -or $charCode -eq 13 -or $charCode -eq 9) {
                $newContent += $char
            }
            else {
                # Remplacer les caracteres speciaux communs
                $replacement = switch ($char) {
                    'à' { 'a'; break }
                    'â' { 'a'; break }
                    'ä' { 'a'; break }
                    'é' { 'e'; break }
                    'è' { 'e'; break }
                    'ê' { 'e'; break }
                    'ë' { 'e'; break }
                    'î' { 'i'; break }
                    'ï' { 'i'; break }
                    'ô' { 'o'; break }
                    'ö' { 'o'; break }
                    'ù' { 'u'; break }
                    'û' { 'u'; break }
                    'ü' { 'u'; break }
                    'ç' { 'c'; break }
                    'ÿ' { 'y'; break }
                    default { ''; break }  # Supprimer (emojis, etc.)
                }
                $newContent += $replacement
                $totalChanges++
            }
        }
        
        if ($newContent -ne $original) {
            Set-Content $file.FullName $newContent -NoNewline -Encoding UTF8
            $count++
            Write-Host "Corrige: $($file.Name) ($totalChanges changements)"
            $totalChanges = 0
        }
    }
    catch {
        Write-Host "Erreur sur $($file.Name): $_"
    }
}

Write-Host "`nTotal: $count fichiers corriges"
