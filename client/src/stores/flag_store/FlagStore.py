import threading
from queue import Queue
from typing import List

from common import Flag


class FlagStore:
    """
    A class for storing and managing a queue of Flag objects in a thread-safe manner.

    Attributes:
        flags (Queue[Flag]): The queue of Flag objects stored in the store.
        seen_flags (set[str]): A set of flag strings that have already been added to the store.
        lock (threading.RLock): A reentrant lock for synchronizing access to the store.
    """

    def __init__(self):
        """Initialize an empty FlagStore."""
        self.flags = Queue()
        self.seen_flags = set()
        self.lock = threading.RLock()

    def add_flag(self, flag: Flag) -> None:
        """
        Add a Flag object to the store, if it has not already been added.

        Args:
            flag (Flag): The flag to add to the store.
        """
        with self.lock:
            if flag.flag not in self.seen_flags:
                self.flags.put(flag)
                self.seen_flags.add(flag.flag)

    def remove_flag(self, num_flags: int) -> List[Flag]:
        """
        Remove and return the oldest Flag object from the store.

        Returns:
            A list of the num_flags oldest Flag objects in the store.
        """
        removed_flags = []
        with self.lock:
            for _ in range(num_flags):
                removed_flags.append(self.flags.get())
        return removed_flags

    def get_flags(self) -> List[Flag]:
        """
        Get a list of all the Flag objects in the store.

        Returns:
            A list of all the Flag objects in the store.
        """
        with self.lock:
            return list(self.flags.queue)
