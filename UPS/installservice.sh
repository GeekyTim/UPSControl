#!/usr/bin/env bash

sudo touch /lib/systemd/system/UPS.service
echo "
[Unit]
Description=UPS Service
After=multi-user.target

[Service]
Type=idle
User=${USER}
ExecStart=/usr/bin/python3 /home/${USER}/UPS/ups.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
" | sudo tee /lib/systemd/system/UPS.service > /dev/null

echo "Installing required libraries"
sudo apt update
sudo apt install python3-pip
sudo pip3 install vcgencmd

echo "Change unit file permissions"
sudo chmod 644 /lib/systemd/system/UPS.service
echo "Reload Daemon"
sudo systemctl daemon-reload
echo "Enable UPS.service"
sudo systemctl enable UPS.service
echo "Start UPS.service"
sudo systemctl start UPS.service

