import threading
from typing import Dict


class ProcessStore:
    """
    A class for storing and managing a dictionary of running exploit instances in a thread-safe manner.

    Attributes:
        processes (Dict[str, Process]): A dictionary mapping exploit names to running exploit instances.
        stats (Dict[str, Dict[str, int]]): A dictionary mapping exploit names to dictionaries of statistics.
        counter (int): A counter for the number of running exploit instances.
        lock (threading.RLock): A reentrant lock for synchronizing access to the store.
    """

    def __init__(self):
        """Initialize an empty ProcessStore."""
        self.processes = {}
        self.stats = {}
        self.counter = 0
        self.lock = threading.RLock()

    def add_process(self, name: str, process) -> None:
        """
        Add a running exploit instance to the store.

        Args:
            name (str): The name of the exploit.
            process (Process): The running exploit instance.
        """
        with self.lock:
            self.processes[name] = process
            self.stats[name] = self.stats.get(name, {'killed': 0, 'completed': 0})
            self.counter += 1

    def remove_process(self, name: str, status: str):
        """
        Remove and return a running exploit instance from the store, and update the corresponding statistics.

        Args:
            name (str): The name of the exploit.
            status (str): The status of the exploit instance ('killed' or 'completed').

        Returns:
            The running exploit instance corresponding to the given name.
        """
        with self.lock:
            process = self.processes.pop(name)
            self.stats[name][status] += 1
            self.counter -= 1
            return process

    def get_processes(self) -> Dict[str, any]:
        """
        Get a dictionary mapping exploit names to running exploit instances.

        Returns:
            A dictionary mapping exploit names to running exploit instances.
        """
        with self.lock:
            return self.processes.copy()

    def get_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Get a dictionary mapping exploit names to dictionaries of statistics.

        Returns:
            A dictionary mapping exploit names to dictionaries of statistics.
        """
        with self.lock:
            return self.stats.copy()

    def get_counter(self) -> int:
        """
        Get the current number of running exploit instances.

        Returns:
            The current number of running exploit instances.
        """
        with self.lock:
            return self.counter
