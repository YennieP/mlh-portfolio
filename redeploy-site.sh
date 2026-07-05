#!/bin/bash

tmux kill-server 2>/dev/null

cd ~/mlh-portfolio

git fetch && git reset origin/main --hard

source venv/bin/activate
pip install -r requirements.txt

tmux new-session -d -s flask "cd ~/mlh-portfolio && source venv/bin/activate && flask run --host=0.0.0.0"
