@echo off
call venv\Scripts\activate.bat
pytest -v tests/
pause