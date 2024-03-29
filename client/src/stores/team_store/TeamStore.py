import threading
from typing import Dict

from common import Team
from config import Config
from loguru import logger


class TeamStore:
    """
    A class for storing and managing a dictionary of `Team` objects in a thread-safe manner.

    Attributes:
        teams (Dict[str, Team]): A dictionary mapping team names to `Team` objects.
        lock (threading.RLock): A reentrant lock for synchronizing access to the store.
    """

    def __init__(self, config: Config = None):
        """Initialize an empty TeamStore."""
        self.teams = {}
        self.lock = threading.RLock()
        if config:
            for team in config.get_teams():
                self.add_team(team)
    

    def add_team(self, team: Team) -> None:
        """
        Add a `Team` object to the store.

        Args:
            team (Team): The `Team` object to add.
        """
        with self.lock:
            self.teams[team.name] = team
        logger.debug("Added team " + team.country)

    def remove_team(self, name: str) -> Team:
        """
        Remove and return a `Team` object from the store.

        Args:
            name (str): The name of the team.

        Returns:
            The `Team` object corresponding to the given name.
        """
        with self.lock:
            return self.teams.pop(name)

    def get_teams(self) -> Dict[str, Team]:
        """
        Get a dictionary mapping team names to `Team` objects.

        Returns:
            A dictionary mapping team names to `Team` objects.
        """
        with self.lock:
            return self.teams.copy()
