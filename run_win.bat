@echo off
echo Installing requirements / checking for updates...
echo.
python -m pip install --upgrade -r requirements.txt
echo.
echo.
echo Running the bot...
echo.
python bot.py
