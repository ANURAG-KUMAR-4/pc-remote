Set WinScriptHost = CreateObject("WScript.Shell")
' Executes the script inside your dedicated virtual environment silently
WinScriptHost.Run "cmd.exe /c cd /d C:\Users\anura\pc-remote && .venv\Scripts\python.exe app.py", 0, False
Set WinScriptHost = Nothing