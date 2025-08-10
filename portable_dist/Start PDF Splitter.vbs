' Simple PDF Splitter - Silent Launcher
' This runs the application without showing any terminal window

Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the app directory
WshShell.CurrentDirectory = strPath

' Check if dependencies are installed
depsFile = strPath & "\python_embedded\.deps_installed"
If Not objFSO.FileExists(depsFile) Then
    ' First run - install dependencies (this may take 30 seconds)
    MsgBox "First time setup - this will take about 30 seconds." & vbCrLf & vbCrLf & "Click OK to continue.", vbInformation, "Simple PDF Splitter"
    WshShell.Run "python_embedded\python.exe -m pip install --no-warn-script-location -r app\requirements.txt", 0, True
    Set objFile = objFSO.CreateTextFile(depsFile, True)
    objFile.Close
End If

' Run the application silently
WshShell.Run "python_embedded\python.exe app\main.py", 0, False

' Wait a moment for the server to start
WScript.Sleep 3000

' Open the browser
WshShell.Run "http://localhost:5000"

' Show tray notification
MsgBox "Simple PDF Splitter is running!" & vbCrLf & vbCrLf & "Your browser should open automatically." & vbCrLf & "If not, go to: http://localhost:5000" & vbCrLf & vbCrLf & "To stop: Close this message and the browser tab.", vbInformation, "Simple PDF Splitter"