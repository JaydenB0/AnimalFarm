from threading import RLock
from typing import List

from common import Team


class Config:
  """
  """
  def __init__(self, exploit_dir = "../exploits", teams = [], attack_period = 10):
    self.teams = teams # initial teams
    self.exploit_dir = exploit_dir
    self.attack_period = attack_period
    self.lock = RLock()

  def get_attack_period(self):
    return self.attack_period
  def set_attack_period(self, secs: int):
    with self.lock:
      self.attack_period = secs

  def get_teams(self):
    return self.teams

  def get_exploit_dir(self):
    return self.exploit_dir
  def set_exploit_dir(self, exploit_dir):
    with self.lock:
        self.exploit_dir = exploit_dir
