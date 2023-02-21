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
" | sudo tee /lib/systemd/system/UPS.service

sudo chmod 644 /lib/systemd/system/UPS.service
sudo systemctl daemon-reload
sudo systemctl enable UPS.service
sudo systemctl start UPS.service

