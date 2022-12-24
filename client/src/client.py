import time

import pyfiglet
from manager import Manager

client_ver = "0.0.2"

def printHeader():
    header = pyfiglet.figlet_format("AnimalFarm")
    print(header)
    print("Client Version: " + client_ver)

if __name__ == "__main__":
    printHeader()
    mgr = Manager("/workspaces/AnimalFarm/client/exploits")
    time.sleep(1000)