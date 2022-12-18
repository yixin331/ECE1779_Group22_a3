#! /bin/bash
pip install -r requirements.txt
tmux new -d -s autoscaler "python3 A_3/autoscaler/run.py"
python3 A_3/manager/run.py
pkill -f tmux
echo "Server ended!"