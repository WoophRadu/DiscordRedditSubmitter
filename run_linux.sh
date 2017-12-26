#!/bin/bash
echo "Installing requirements / checking for updates..."
echo -e "\n"
python3.6 -m pip install --upgrade -r requirements.txt
echo -e "\n\n"
echo "Running the bot..."
python3.6 bot.py