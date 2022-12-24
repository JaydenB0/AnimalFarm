import os

from attacker import Attacker
from common.exploit import Exploit
from loguru import logger
from stores.exploit_store import ExploitStore
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class Watcher:
    """
    A class that uses the `watchdog` library to monitor a directory for new files and create `Exploit` objects for each new file, adding them to an `ExploitStore`.

    Attributes:
        directory (str): The directory to monitor for new files.
        store (ExploitStore): The `ExploitStore` to add new `Exploit` objects to.
        observer (Observer): The `Observer` object from the `watchdog` library.
    """

    def __init__(self, directory: str, exploit_store: ExploitStore, attacker: Attacker) -> None:
        """
        Initialize a `Watcher` object.

        Args:
            directory (str): The directory to monitor for new files.
            exploit_store (ExploitStore): The `ExploitStore` to update with new exploits.
            manager (CTFManager): The `CTFManager` to launch the new exploit immediately.
        """
        self.directory = directory
        self.exploit_store = exploit_store
        self.observer = Observer()
        self.attacker = attacker
        self.event_handler = EventHandler(self.exploit_store, self.attacker)

    def run(self) -> None:
        """Start monitoring the directory for new files."""
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()

class EventHandler(FileSystemEventHandler):
    """
    A `FileSystemEventHandler` class that creates `Exploit` objects for new files and adds them to an `ExploitStore`.
    """

    def __init__(self, store: ExploitStore, attacker: Attacker) -> None:
        """
        Initialize a `NewFileHandler` object.

        Args:
            store (ExploitStore): The `ExploitStore` to add new `Exploit` objects to.
            attacker (Attacker): The `Attacker` to launch the new exploit immediately.
        """
        self.store = store
        self.attacker = attacker

    def on_any_event(self, event: FileSystemEvent) -> None:
        """
        Create an `Exploit` object for a new file and add it to the `ExploitStore`.

        Args:
            event (FileCreatedEvent): The `FileCreatedEvent` object representing the new file.
        """
        if event.is_directory:
            return
        elif event.event_type in ('created', 'modified'):
            # Add the new exploit to the exploit store
            logger.debug("Found new file!")
            if (event.event_type != 'modified'):
                exploit = Exploit(os.path.basename(event.src_path), event.src_path)
                self.store.add_exploit(exploit)

            # Launch the exploit immediately
            self.attacker.launch_exploits()
            
        elif event.event_type in ('deleted', 'moved'):
            logger.debug(event.src_path)
            self.store.remove_exploit(self.store.find(event.src_path))

