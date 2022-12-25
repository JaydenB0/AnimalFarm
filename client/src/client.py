import time

import pyfiglet
from manager import Manager

CLIENT_VER = "0.0.3"

def printHeader():
    header = pyfiglet.figlet_format("AnimalFarm")
    print(header)
    print("Client Version: " + CLIENT_VER)

if __name__ == "__main__":
    printHeader()
    mgr = Manager("/workspaces/AnimalFarm/client/exploits")
    time.sleep(1000)