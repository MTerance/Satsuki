$files = Get-ChildItem "C:\Users\sshom\source\repos\Satsuki\Satsuki" -Recurse -Include "*.cs" -Exclude "*AssemblyInfo.cs","*AssemblyAttributes.cs"

# Table de remplacement exacte
$replacements = @{
    [char]0x00E0 = 'a'  # à
    [char]0x00E2 = 'a'  # â  
    [char]0x00E4 = 'a'  # ä
    [char]0x00E9 = 'e'  # é
    [char]0x00E8 = 'e'  # è
    [char]0x00EA = 'e'  # ê
    [char]0x00EB = 'e'  # ë
    [char]0x00EE = 'i'  # î
    [char]0x00EF = 'i'  # ï
    [char]0x00F4 = 'o'  # ô
    [char]0x00F6 = 'o'  # ö
    [char]0x00F9 = 'u'  # ù
    [char]0x00FB = 'u'  # û
    [char]0x00FC = 'u'  # ü
    [char]0x00FF = 'y'  # ÿ
    [char]0x00E7 = 'c'  # ç
}

# Liste d'emojis  supprimer (codes UTF-16)
$emojisToRemove = @(
    0x1F3AC, # ??
    0x1F3AE, # ??
    0x1F4CA, # ??
    0x2705,  # ?
    0x274C,  # ?
    0x2699,  # ??
    0x1F4DC, # ??
    0x1F44B, # ??
    0x1F9F9, # ??
    0x1F37D,  # ???
    0x1F4F7, # ??
    0x1F5D1, # ???
    0x1F4AC, # ??
    0x1F41B, # ??
    0x1F310, # ??
    0x1F6D1, # ??
    0x1F464, # ??
    0x1F3D7, # ???
    0x1F3A5, # ??
    0x1F527, # ??
    0x1F4E6, # ??
    0x1F4A4, # ??
    0x1F91D, # ??
    0x1F504, # ??
    0x1F4FA, # ??
    0x1F680, # ??
    0x2728   # ?
)

$count = 0

foreach ($file in $files) {
    try {
        $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
        $text = [System.Text.Encoding]::UTF8.GetString($bytes)
        $original = $text
        
        # Remplacer les caracteres accentues
        $newText = ""
        for ($i = 0; $i < $text.Length; $i++) {
            $char = $text[$i]
            if ($replacements.ContainsKey($char)) {
                $newText += $replacements[$char]
            } else {
                $newText += $char
            }
        }
        
        # Supprimer les emojis
        foreach ($emojiCode in $emojisToRemove) {
            $emoji = [char]::ConvertFromUtf32($emojiCode)
            $newText = $newText.Replace($emoji, '')
        }
        
        if ($newText -ne $original) {
            [System.IO.File]::WriteAllText($file.FullName, $newText, [System.Text.UTF8Encoding]::new($false))
            $count++
            Write-Host "Corrige: $($file.Name)"
        }
    }
    catch {
        Write-Host "Erreur sur $($file.Name): $_"
    }
}

Write-Host "Total: $count fichiers corriges"
