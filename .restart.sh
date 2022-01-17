#!/bin/bash

alias restartapi='
sudo systemctl stop api
sudo systemctl disable api
sudo systemctl daemon-reload
sudo systemctl start api
sudo systemctl enable api
sudo systemctl restart nginx
'
