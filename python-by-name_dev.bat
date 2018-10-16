set PYTHON_HOME=%~dp0\venv\Scripts
set PYTHON_NAME=%1.exe
set DEV_SERVER_HOME=%C:\Luna_Dev
copy "%PYTHON_HOME%\python.exe" "%DEV_SERVER_HOME%\%PYTHON_NAME%"
set args=%*
set args=%args:* =%
"%DEV_SERVER_HOME%\%PYTHON_NAME%" %args%