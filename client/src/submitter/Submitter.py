import threading

import requests
from attacker import Attacker
from stores import FlagStore


class Submitter:
  """A class that posts the flag to the server."""
  def __init__(self, attacker: Attacker, flag_store: FlagStore, url: str) -> None:
    """
    Initialize a `FlagPoster` object.

    Args:
    ctf_manager (CTFManager): The `CTFManager` to start.
    flag_store (FlagStore): The `FlagStore` to retrieve the flags from.
    url (str): The URL of the web server to post the flags to.
    """

    self.attacker = attacker
    self.flag_store = flag_store
    self.url = url
    self.timer = None

  def start(self) -> None:
    """Schedule a recurring event to post the flags to the web server every 10 seconds."""
    self.timer = threading.Time(10.0, self.post_flags)
    self.timer.start()

  def stop(self) -> None:
    """Stop submitting flags and cancel the recurring event."""
    self.timer.cancel()

  def post_flag(self) -> None:
    """Post all flags in the queue to the server."""
    flags = self.flag_store.get_flags()
    for flag in flags:
      data = {'flag': flag.flag, 'team': flag.team, 'exploit': flag.exploit}
      success = False
      while not success:
        try:
          response = requests.post(self.url, data=data)
          if response.status_code == 200:
            success = True
        except ConnectionError:
          # If there is a connection error, put the flag back in the queue and try again
          self.flag_store.add_flag(flag)
