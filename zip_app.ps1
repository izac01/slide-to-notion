# zip_app.ps1
# Script to zip your project code excluding unnecessary folders.

$ProjectRoot = "C:\Users\iZac\Documents\slide-to-notion"
$OutputZip   = Join-Path $ProjectRoot "slide_to_notion_project.zip"

Write-Host "Creating project zip..."

# Exclude these folders & extensions
$ExcludeDirs = @("metagpt", ".venv", "logs", "output_project", "__pycache__")
$ExcludeExts = @(".pyc", ".pyo", ".log", ".zip")

# Collect files to include
$Files = Get-ChildItem -Path $ProjectRoot\workspace -Recurse -File | Where-Object {
    ($ExcludeDirs -notcontains $_.DirectoryName.Split('\')[-1]) -and
    ($ExcludeExts -notcontains $_.Extension)
}

# Remove old zip if it exists
if (Test-Path $OutputZip) {
    Remove-Item $OutputZip -Force
}

# Create zip
Compress-Archive -Path $Files.FullName -DestinationPath $OutputZip -Force

Write-Host "✅ Project zipped successfully to $OutputZip"
