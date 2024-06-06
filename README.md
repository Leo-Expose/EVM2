# EVM 2 


## Description
This project is an electronic voting machine (EVM) system implemented using Arduino and Python. It includes a GUI for starting, pausing, and stopping the voting process, a web server for displaying live results, and functionality for exporting the final results to a document. 
This is the final version of my EVM Project

## Requirements

- Python 3.7 or later (3.11 is preferred)
- Arduino board
- Required Python libraries (listed in `resources/requirements.txt`)

## Setup

1. **Clone the repository and navigate to the project directory:**
    ```sh
    git clone https://github.com/Leo-Expose/EVM2.git
    cd EVM2
    ```

2. **Configure your network interface to use the IP address `192.168.1.1`:**
    - Open **Control Panel**.
    - Go to **Network and Sharing Center**.
    - Click on **Change adapter settings**.
    - Right-click on your active network connection and select **Properties**.
    - Select **Internet Protocol Version 4 (TCP/IPv4)** and click **Properties**.
    - Select **Use the following IP address** and enter:
      - **IP address**: `192.168.1.1`
      - **Subnet mask**: `255.255.255.0`

3. **Connect the Arduino to the correct COM port (`COM4` in this case).**

## Running the Project

1. **Initialize the setup and start the voting server:**
    - Use the provided `Initialize.bat` file:
      ```sh
      Initialize.bat
      ```

2. **Access the web server to view live voting results:**
    - For total results:
      ```plaintext
      http://192.168.1.1:4200/votes
      ```
    - For the latest vote:
      ```plaintext
      http://192.168.1.1:4200/latest_vote
      ```

3. **Use the GUI to control voting:**
    - The GUI window will have "Start Voting", "Pause Voting", and "Stop Voting" buttons.

## Notes

- Ensure that the serial port (`COM4`) in the Python script matches the one used by your Arduino board.
- The Flask server is accessible on the IP address `192.168.1.1` with port `4200` for total results and port `7000` for the latest vote
- Make sure to configure the network IP settings in windows

  # With great votes comes great responsibility
  - Uncle Ben Dover
