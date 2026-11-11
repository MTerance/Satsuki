param(
    [string]$BaseUrl = 'http://localhost:8092',
    [string]$AdminKey = $env:AKIBA_ADMIN_API_KEY
)
$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($AdminKey)) {
    throw 'Définir AKIBA_ADMIN_API_KEY dans cette session PowerShell.'
}
$headers = @{ 'X-Akiba-Admin-Key' = $AdminKey }

$unauthorized = Invoke-WebRequest -Uri "$BaseUrl/api/catalog/games" -SkipHttpErrorCheck
if ([int]$unauthorized.StatusCode -ne 401) {
    throw "Sans clé API, le code attendu est 401, reçu $($unauthorized.StatusCode)"
}

$summaries = @(Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/catalog/games" -Headers $headers)
Write-Host "Catalogue chargé: $($summaries.Count) Game(s)"
foreach ($g in $summaries) {
    if ($null -eq $g.id -or $null -eq $g.name -or
        $null -eq $g.roundCount -or $null -eq $g.questionCount) {
        throw 'GameSummaryDto incomplet.'
    }
}

if ($summaries.Count -gt 0) {
    $id = [long]$summaries[0].id
    $full = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/catalog/games/$id" -Headers $headers
    if ([long]$full.id -ne $id -or $null -eq $full.rounds) {
        throw 'GameFullDto invalide ou incomplet.'
    }
    foreach ($round in $full.rounds) {
        foreach ($q in $round.questions) {
            if ($q.type -eq 'QCM' -and ($null -eq $q.qcm -or $null -eq $q.qcm.answers)) {
                throw 'QCM complet non résolu.'
            }
            if ($q.type -eq 'QuestionAnswer' -and $null -eq $q.questionAnswer) {
                throw 'QuestionAnswer non résolue.'
            }
        }
    }
    Write-Host "Game complet validé: $($full.name)"
} else {
    Write-Warning 'Aucun Game présent : le test Game complet nécessite un Game de test.'
}

$notFound = Invoke-WebRequest -Uri "$BaseUrl/api/catalog/games/9223372036854775807" -Headers $headers -SkipHttpErrorCheck
if ([int]$notFound.StatusCode -ne 404) {
    throw "Game inexistant : HTTP 404 attendu, reçu $($notFound.StatusCode)"
}
Write-Host 'Contrôles HTTP PASS (sans modification des données).'
