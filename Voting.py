import serial
import time
import os
import json
import logging
from flask import Flask, jsonify, render_template
from threading import Thread
import tkinter as tk
from tkinter import messagebox
from docx import Document

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load configuration
config_file_path = os.path.join('resources', 'config.json')
with open(config_file_path) as config_file:
    config = json.load(config_file)

SERIAL_PORT = config['SERIAL_PORT'] #9600
BAUD_RATE = config['BAUD_RATE']
BACKUP_FILE = os.path.expanduser(config['BACKUP_FILE'])
RESULT_FILE = os.path.expanduser(config['RESULT_FILE'])
DOC_FILE = os.path.expanduser(config['DOC_FILE'])

# Candidate names 
# I won an award for naming
candidates = ["A", "B", "C", "X", "Y", "Z"]
votes = {candidate: 0 for candidate in candidates}
last_vote = None

# Load existing votes from backup file
if os.path.exists(BACKUP_FILE):
    with open(BACKUP_FILE, 'r') as f:
        for line in f:
            name, vote_count = line.strip().split(',')
            votes[name] = int(vote_count)

# Initialize serial connection to the computers heart for efficiency
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
except serial.SerialException as e:
    logging.error(f"Failed to connect to serial port: {e}")
    raise

def save_backup():
    with open(BACKUP_FILE, 'w') as f:
        for name, count in votes.items():
            f.write(f"{name},{count}\n")

def export_results():
    doc = Document()
    doc.add_heading('Voting Results', 0)
    for name, count in votes.items():
        doc.add_paragraph(f"{name}: {count} votes")
    doc.save(DOC_FILE)
    logging.info(f"Results saved to {DOC_FILE}")

def print_results():
    with open(RESULT_FILE, 'w') as f:
        for name, count in votes.items():
            f.write(f"{name}: {count} votes\n")
    logging.info(f"Results saved to {RESULT_FILE}")

def start_voting():
    global running
    running = True
    try:
        while running:
            if ser.in_waiting > 0:
                vote = ser.readline().decode().strip()
                if vote.startswith("Vote: "):
                    candidate_index = int(vote.split(" ")[1])
                    candidate_name = candidates[candidate_index]
                    votes[candidate_name] += 1
                    global last_vote
                    last_vote = candidate_name
                    logging.info(f"{candidate_name} received a vote. Total now: {votes[candidate_name]}")
                    save_backup()
            time.sleep(0.1)
    except Exception as e:
        logging.error(f"Error during voting: {e}")
    finally:
        ser.close()

def pause_voting():
    global running
    running = False
    logging.info("Voting paused.")

def resume_voting():
    global voting_thread
    global running
    if not running:
        running = True
        voting_thread = Thread(target=start_voting)
        voting_thread.start()
    logging.info("Voting resumed.")

def stop_voting():
    global running
    running = False
    messagebox.showinfo("Voting Stopped", "Voting has been stopped and results exported.")
    export_results()
    root.destroy()

# Flask app setup & drinking
app = Flask(__name__)

@app.route('/votes')
def get_votes():
    return render_template('votes.html', votes=votes, last_vote=last_vote)

@app.route('/latest_vote')
def latest_vote():
    return render_template('latest_vote.html', last_vote=last_vote)

def start_flask():
    app.run(debug=True, use_reloader=False, host='192.168.1.1', port=4200)

# Start Flask server in a separate thread because facebook doesn't have enough money
flask_thread = Thread(target=start_flask)
flask_thread.start()

# Tkinter GUI setup - Start/Stop/Pause. I love Helvetica
root = tk.Tk()
root.title("Voting Control")

start_button = tk.Button(root, text="Start Voting", command=resume_voting, font=('Helvetica', 16))
start_button.pack(pady=10)

pause_button = tk.Button(root, text="Pause Voting", command=pause_voting, font=('Helvetica', 16))
pause_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Voting", command=stop_voting, font=('Helvetica', 16))
stop_button.pack(pady=10)

root.geometry("300x250")
root.protocol("WM_DELETE_WINDOW", stop_voting)

# Start the voting process
voting_thread = Thread(target=start_voting)
voting_thread.start()

# This part is essential but I have no idea why
root.mainloop()
