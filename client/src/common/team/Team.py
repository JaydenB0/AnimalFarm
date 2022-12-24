class Team:
    """
    A class representing a team in a Capture-the-Flag competition.

    Attributes:
        name (str): The name of the team.
        ip (str): The IP address of the team.
        country (str): The country of the team.
    """

    def __init__(self, name: str, ip: str, country: str) -> None:
        """
        Initialize a Team object.

        Args:
            name (str): The name of the team.
            ip (str): The IP address of the team.
            country (str): The country of the team.
        """
        self.name = name
        self.ip = ip
        self.country = country

    def __repr__(self) -> str:
        """
        Return a string representation of the Team object.

        Returns:
            A string representation of the Team object.
        """
        return f'Team(name={self.name}, ip={self.ip}, country={self.country})'
