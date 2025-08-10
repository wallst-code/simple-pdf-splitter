# Simple PDF Splitter - PowerShell Launcher
# Provides the cleanest user experience

Add-Type -AssemblyName System.Windows.Forms

# Create a simple splash screen
$splash = New-Object System.Windows.Forms.Form
$splash.Text = "Simple PDF Splitter"
$splash.Size = New-Object System.Drawing.Size(400,200)
$splash.StartPosition = "CenterScreen"
$splash.FormBorderStyle = "FixedDialog"
$splash.MaximizeBox = $false
$splash.MinimizeBox = $false

$label = New-Object System.Windows.Forms.Label
$label.Text = "Starting Simple PDF Splitter...`n`nYour browser will open automatically.`n`nThis window will close in a moment."
$label.Size = New-Object System.Drawing.Size(380,100)
$label.Location = New-Object System.Drawing.Point(10,30)
$label.TextAlign = "MiddleCenter"
$splash.Controls.Add($label)

$splash.Show()
[System.Windows.Forms.Application]::DoEvents()

# Start the application in background
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check for first run
$depsFile = "$scriptPath\python_embedded\.deps_installed"
if (-not (Test-Path $depsFile)) {
    $label.Text = "First time setup...`n`nInstalling components (30 seconds)...`n`nPlease wait."
    [System.Windows.Forms.Application]::DoEvents()
    
    & "$scriptPath\python_embedded\python.exe" -m pip install --no-warn-script-location -r "$scriptPath\app\requirements.txt" 2>$null
    New-Item -Path $depsFile -ItemType File -Force | Out-Null
}

# Start the Python app hidden
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "$scriptPath\python_embedded\python.exe"
$psi.Arguments = "$scriptPath\app\main.py"
$psi.WindowStyle = "Hidden"
$psi.CreateNoWindow = $true
$process = [System.Diagnostics.Process]::Start($psi)

# Wait for server to start
Start-Sleep -Seconds 3

# Open browser
Start-Process "http://localhost:5000"

# Close splash screen
$splash.Close()

# Show system tray notification
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.Visible = $true
$notify.ShowBalloonTip(5000, "Simple PDF Splitter", "Application is running at http://localhost:5000", [System.Windows.Forms.ToolTipIcon]::Info)
Start-Sleep -Seconds 5
$notify.Dispose()