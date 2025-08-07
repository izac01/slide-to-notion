param (
    [string]$Workspace = "C:\Users\iZac\Documents\slide-to-notion\workspace",
    [string]$OutputDir = "C:\Users\iZac\Documents\slide-to-notion"
)

Write-Host "Scanning workspace: $Workspace"

# Ensure output directory exists
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

# Save the project tree
$projectTree = Join-Path $OutputDir "project_tree.txt"
Get-ChildItem -Path $Workspace -Recurse |
    ForEach-Object { $_.FullName.Replace("$Workspace\", "") } |
    Out-File $projectTree -Encoding UTF8
Write-Host "Project tree saved to $projectTree"

# Collect duplicate .py files
$filesByName = Get-ChildItem -Path $Workspace -Recurse -Filter *.py |
    Group-Object -Property Name | Where-Object { $_.Count -gt 1 }

if ($filesByName.Count -eq 0) {
    Write-Host "No duplicate filenames found for diffing."
}
else {
    Write-Host "Found $($filesByName.Count) duplicate filenames. Running diffs..."

    foreach ($group in $filesByName) {
        $fileName = $group.Name
        $diffReport = Join-Path $OutputDir ("diff_" + $fileName + "_report.txt")

        $refFile = $group.Group[0].FullName
        for ($i = 1; $i -lt $group.Group.Count; $i++) {
            $cmpFile = $group.Group[$i].FullName
            Compare-Object (Get-Content $refFile) (Get-Content $cmpFile) -SyncWindow 10 |
                Out-File -Append $diffReport -Encoding UTF8
            Add-Content -Path $diffReport -Value "`n--- Compared $refFile vs $cmpFile ---`n" -Encoding UTF8
            Write-Host "Diffed $fileName -> $diffReport"
        }
    }

    Write-Host "Diff reports saved in $OutputDir"
}

Write-Host "Analysis complete. Provide project_tree.txt and diff reports to Copilot."
