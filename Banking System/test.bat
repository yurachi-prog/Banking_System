@echo off
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" test_suite.py %*
) else (
    python test_suite.py %*
)
pause
