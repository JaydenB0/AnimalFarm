import time

import pyfiglet
from common import Team
from manager import Manager

CLIENT_VER = "0.0.4"
EXPLOIT_DIR = "/workspaces/AnimalFarm/client/exploits"
TEAMS = []

def print_header():
    header = pyfiglet.figlet_format("AnimalFarm")
    print(header)
    print("Client Version: " + CLIENT_VER)

if __name__ == "__main__":
    print_header()
    mgr = Manager(EXPLOIT_DIR, TEAMS)
    time.sleep(1000)