# Script PowerShell de deploiement automatique pour l'addon City Block Generator
# Copie automatiquement les fichiers Python vers le repertoire des addons de Blender

param(
    [switch]$Force,
    [switch]$Backup
)

# Configuration des chemins
$SourceDir = "C:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12"
$TargetDir = "C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\city_block_generator_6_12"

# Fichiers Python a copier
$PythonFiles = @(
    "__init__.py",
    "generator.py", 
    "operators.py",
    "ui.py",
    "reload_addon.py"
)

function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    
    $colors = @{
        "Green" = "Green"
        "Red" = "Red"
        "Yellow" = "Yellow"
        "Cyan" = "Cyan"
        "Magenta" = "Magenta"
        "White" = "White"
    }
    
    Write-Host $Text -ForegroundColor $colors[$Color]
}

function Ensure-TargetDirectory {
    try {
        if (-not (Test-Path $TargetDir)) {
            New-Item -Path $TargetDir -ItemType Directory -Force | Out-Null
            Write-ColorText "Repertoire de destination cree: $TargetDir" "Green"
        } else {
            Write-ColorText "Repertoire de destination verifie: $TargetDir" "Green"
        }
        return $true
    }
    catch {
        Write-ColorText "Erreur creation repertoire de destination: $($_.Exception.Message)" "Red"
        return $false
    }
}

function Backup-ExistingAddon {
    if (Test-Path $TargetDir) {
        $BackupDir = "$TargetDir" + "_backup_" + (Get-Date -Format "yyyyMMdd_HHmmss")
        try {
            Copy-Item -Path $TargetDir -Destination $BackupDir -Recurse -Force
            Write-ColorText "Sauvegarde creee: $BackupDir" "Cyan"
            return $true
        }
        catch {
            Write-ColorText "Impossible de creer la sauvegarde: $($_.Exception.Message)" "Yellow"
            return $false
        }
    }
    return $true
}

function Copy-PythonFiles {
    $CopiedFiles = 0
    $FailedFiles = 0
    
    Write-ColorText "Copie des fichiers Python..." "Cyan"
    
    foreach ($filename in $PythonFiles) {
        $SourcePath = Join-Path $SourceDir $filename
        $TargetPath = Join-Path $TargetDir $filename
        
        try {
            if (Test-Path $SourcePath) {
                # Copier le fichier
                Copy-Item -Path $SourcePath -Destination $TargetPath -Force
                
                # Verifier que la copie a reussi
                if (Test-Path $TargetPath) {
                    $SourceSize = (Get-Item $SourcePath).Length
                    $TargetSize = (Get-Item $TargetPath).Length
                    
                    if ($SourceSize -eq $TargetSize) {
                        Write-ColorText "$filename copie ($SourceSize bytes)" "Green"
                        $CopiedFiles++
                    } else {
                        Write-ColorText "$filename copie mais tailles differentes (source: $SourceSize, cible: $TargetSize)" "Yellow"
                        $FailedFiles++
                    }
                } else {
                    Write-ColorText "$filename : echec de la copie" "Red"
                    $FailedFiles++
                }
            } else {
                Write-ColorText "$filename : fichier source introuvable" "Yellow"
                $FailedFiles++
            }
        }
        catch {
            Write-ColorText "Erreur lors de la copie de $filename : $($_.Exception.Message)" "Red"
            $FailedFiles++
        }
    }
    
    return $CopiedFiles, $FailedFiles
}

function Verify-Installation {
    Write-ColorText "Verification de l'installation..." "Cyan"
    
    $AllGood = $true
    foreach ($filename in $PythonFiles) {
        $TargetPath = Join-Path $TargetDir $filename
        if (Test-Path $TargetPath) {
            Write-ColorText "$filename present" "Green"
        } else {
            Write-ColorText "$filename manquant" "Red"
            $AllGood = $false
        }
    }
    
    return $AllGood
}

function Show-Instructions {
    Write-ColorText "DEPLOIEMENT TERMINE AVEC SUCCES!" "Green"
    Write-ColorText "Vous pouvez maintenant:" "Cyan"
    Write-ColorText "   1. Ouvrir Blender" "White"
    Write-ColorText "   2. Aller dans Edit > Preferences > Add-ons" "White"
    Write-ColorText "   3. Rechercher 'City Block Generator'" "White"
    Write-ColorText "   4. Activer l'addon" "White"
    Write-ColorText "   5. Utiliser les boutons de rechargement pour les mises a jour" "White"
    Write-ColorText "Pour les mises a jour futures, relancez ce script!" "Yellow"
}

# === MAIN SCRIPT ===

Write-ColorText "=== DEPLOIEMENT ADDON CITY BLOCK GENERATOR ===" "Magenta"
Write-ColorText "Source: $SourceDir" "White"
Write-ColorText "Destination: $TargetDir" "White"
Write-ColorText ""

# Verifier que le repertoire source existe
if (-not (Test-Path $SourceDir)) {
    Write-ColorText "ERREUR: Repertoire source introuvable: $SourceDir" "Red"
    Read-Host "Appuyez sur Entree pour fermer"
    exit 1
}

# Creer une sauvegarde si demande
if ($Backup) {
    if (-not (Backup-ExistingAddon)) {
        Write-ColorText "Echec de la sauvegarde, continuer quand meme? (O/N)" "Yellow"
        $response = Read-Host
        if ($response -ne "O" -and $response -ne "o") {
            exit 1
        }
    }
}

# Creer le repertoire de destination
if (-not (Ensure-TargetDirectory)) {
    Read-Host "Appuyez sur Entree pour fermer"
    exit 1
}

# Copier les fichiers
$CopiedFiles, $FailedFiles = Copy-PythonFiles

# Verifier l'installation
$Success = Verify-Installation

# Resume
Write-ColorText "=== RESUME DU DEPLOIEMENT ===" "Magenta"
Write-ColorText "Fichiers copies avec succes: $CopiedFiles" "Green"
Write-ColorText "Fichiers en echec: $FailedFiles" "Red"

if ($Success) {
    Write-ColorText "Installation reussie" "Green"
    Show-Instructions
} else {
    Write-ColorText "Installation echouee" "Red"
    Write-ColorText "DEPLOIEMENT ECHOUE!" "Red"
    Write-ColorText "Verifiez les permissions et les chemins" "Yellow"
}

Write-ColorText "Appuyez sur Entree pour fermer..." "White"
Read-Host
exit $(if ($Success) { 0 } else { 1 })
