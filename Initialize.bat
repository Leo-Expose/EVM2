@echo off
echo Checking Python requirements...
if exist venv (
    echo Virtual environment already exists. Activating...
) else (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r resources\requirements.txt
echo Starting the voting server...
python Voting.py
pause
