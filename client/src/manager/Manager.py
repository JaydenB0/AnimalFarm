from attacker import Attacker
from loguru import logger
from stores import ExploitStore, FlagStore, ProcessStore, TeamStore
from watcher import Watcher


class Manager:
  """
  A class that starts the program.
  """
  def __init__(self, exploit_dir: str):
    flag_store = FlagStore()
    team_store = TeamStore()
    exploit_store = ExploitStore()
    process_store = ProcessStore()
    attacker = Attacker(exploit_dir, exploit_store, team_store, process_store, flag_store)
    watcher = Watcher(exploit_dir, exploit_store, attacker)
    watcher.run()
    logger.debug("Watcher has been initialized.")
    logger.debug("Manager has been initialized.")