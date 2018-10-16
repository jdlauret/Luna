set PYTHON_HOME=%~dp0\venv\Scripts
set PYTHON_NAME=%1.exe
set PROD_SERVER_HOME=%C:\Luna_Production
copy "%PYTHON_HOME%\python.exe" "%PROD_SERVER_HOME%\%PYTHON_NAME%"
set args=%*
set args=%args:* =%
"%PROD_SERVER_HOME%\%PYTHON_NAME%" %args%