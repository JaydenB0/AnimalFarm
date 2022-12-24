import datetime


class Flag:
    """
    A class representing a flag captured in a Capture the Flag (CTF) competition.

    Attributes:
        flag (str): The flag string captured from an exploit.
        team (str): The team that got exploited.
        exploit (str): The exploit that was used to capture the flag.
        capture_time (datetime.datetime): The time at which the flag was captured.
    """
    def __init__(self, flag: str, team: str, exploit: str, capture_time: datetime.datetime) -> None:
        """
        Initialize a Flag object.

        Args:
            flag (str): The flag string captured from an exploit.
            team (str): The team that got exploited.
            exploit (str): The exploit that was used to capture the flag.
            capture_time (datetime.datetime): The time at which the flag was captured.
        """
        self.flag = flag
        self.team = team
        self.exploit = exploit
        self.capture_time = capture_time
