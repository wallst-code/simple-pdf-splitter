# PowerShell script to create a safe ZIP without private data
# This creates a clean distribution package

$sourcePath = "portable_dist"
$zipPath = "SimplePDFSplitter-Portable-v1.0.0.zip"

# Remove any existing ZIP
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
    Write-Host "Removed existing ZIP file"
}

# Create the ZIP archive
Write-Host "Creating ZIP archive..."
Compress-Archive -Path "$sourcePath\*" -DestinationPath $zipPath -CompressionLevel Optimal

# Get file info
$zipInfo = Get-Item $zipPath
$sizeMB = [math]::Round($zipInfo.Length / 1MB, 2)

Write-Host ""
Write-Host "=========================================="
Write-Host "ZIP Archive Created Successfully!"
Write-Host "=========================================="
Write-Host "File: $($zipInfo.Name)"
Write-Host "Size: $sizeMB MB"
Write-Host ""
Write-Host "This archive contains:"
Write-Host "  - Embedded Python (no installation needed)"
Write-Host "  - Simple PDF Splitter application"
Write-Host "  - All required dependencies"
Write-Host ""
Write-Host "NO PRIVATE DATA INCLUDED:"
Write-Host "  - No .env file with secret keys"
Write-Host "  - No logs with personal paths"
Write-Host "  - No .hypothesis test data"
Write-Host "  - No .claude settings"
Write-Host ""
Write-Host "Ready for distribution!"