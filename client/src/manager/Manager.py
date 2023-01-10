from typing import Callable

from attacker import Attacker
from common import Team
from config import Config
from loguru import logger
from stores import ExploitStore, FlagStore, ProcessStore, TeamStore
from watcher import Watcher


class Manager:
    """
    A class that starts the program.
    """
    def __init__(self, exploit_dir: str, teams):

        self.config = Config(exploit_dir, teams, 10)

        self.flag_store = FlagStore()
        self.team_store = TeamStore(self.config)
        self.exploit_store = ExploitStore(self.config)
        self.process_store = ProcessStore()
        logger.debug("The stores are initalized.")

        self.attacker = Attacker(self.config, self.exploit_store,
        self.team_store, self.process_store, self.flag_store)
        self.watcher = Watcher(exploit_dir, self.exploit_store, self.attacker)

        self.enabled_modules = [self.attacker, self.watcher]

        logger.debug("Manager has finished setting up.")

    def start(self, module: Callable):
        """
        Start a module
        """
        module.start()

    def start_all(self):
        """
        Starts every module.
        """
        for module in self.enabled_modules:
            self.start(module)

    def stop(self, module: Callable):
        """
        Stop a module
        """
        if module is not None:
          module.stop()
    
    def stop_all(self):
        """
        Stop all running modules
        """
        for module in self.enabled_modules:
            self.stop(module)
