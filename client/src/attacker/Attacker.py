import threading

from common import Exploit
from config import Config
from loguru import logger
from stores import ExploitStore, FlagStore, ProcessStore, TeamStore


class Attacker:
    """
    A class that uses a `Watcher` to monitor a directory for new exploits and a `ProcessStore` to keep track of running exploit instances, launching a thread for each exploit in the `ExploitStore` against every team IP in the `TeamStore` and adding the captured flags to the `FlagStore`.
    """

    def __init__(self, config: Config, exploit_store: ExploitStore, team_store: TeamStore, process_store: ProcessStore, flag_store: FlagStore) -> None:
        """
        Initialize a `Attacker` object.

        Args:
            directory (str): The directory to monitor for new exploits.
            exploit_store (ExploitStore): The `ExploitStore` containing the available exploits.
            team_store (TeamStore): The `TeamStore` containing the target team IPs.
            process_store (ProcessStore): The `ProcessStore` to keep track of running exploit instances.
            flag_store (FlagStore): The `FlagStore` to add captured flags to.
        """
        self.config = config
        self.exploit_store = exploit_store
        self.team_store = team_store
        self.process_store = process_store
        self.flag_store = flag_store
        self.timer = None

    def start(self) -> None:
        """Start monitoring the directory for new exploits."""
        # Schedule a recurring event to launch the exploits every minute
        logger.debug("An attacker instance is running.")
        if self.exploit_store.empty() is not True:
            self.timer = threading.Timer(self.config.get_attack_period(), self.launch_exploits)
            self.timer.start()

    def stop(self) -> None:
        """Stop the attacker and cancel the recurring event."""
        logger.debug("An attacker instance stopped.")
        if self.timer:
            self.timer.cancel()

    def launch_exploits(self) -> None:
        """Launch a thread for each exploit in the `ExploitStore` against every team IP in the `TeamStore`."""
        exploits = self.exploit_store.get_exploits()
        if (len(exploits) == 0):
            return
        teams = self.team_store.get_teams()
        logger.debug("Launching exploits against all IPs")

        for exploit in exploits:
            for team in teams.values():
                thread = threading.Thread(target=self.run_exploit, args=(exploit, team.ip))
                self.process_store.add_process(exploit.name, thread)
                thread.start()
        self.timer = threading.Timer(self.config.get_attack_period(), self.launch_exploits)
        self.timer.start()
        return None

    def run_exploit(self, exploit: Exploit, ip: str) -> None:
        """
        Run an exploit against a target IP and add any captured flags to the `FlagStore`.

        Args:
            exploit (Exploit): The `Exploit` object to run.
            ip (str): The target IP to run the exploit against.
        """
        # Run the exploit and capture the flag, if successful
        flag = exploit.run(ip)

        # Add the flag to the flag store, if it was successfully captured
        if flag:
            self.flag_store.add_flag(flag)