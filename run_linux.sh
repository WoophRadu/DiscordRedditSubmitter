#!/bin/bash
echo "Installing requirements / checking for updates..."
echo -e "\n"
sudo python3 -m pip install --upgrade -r requirements.txt
echo -e "\n\n"
echo "Running the bot..."
python3 bot.py
