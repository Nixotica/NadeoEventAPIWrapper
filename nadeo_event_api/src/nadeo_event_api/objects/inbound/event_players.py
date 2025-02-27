from dataclasses import dataclass
from typing import Any, Dict, List

"""
Example:

  {
    "participant": "05c82ef9-e6a8-4c83-9897-f747ce51fad5",
    "zone": "World",
    "registration": 1619860645,
    "seed": null,
    "addedBy": "6969eb50-f6e3-4fb5-876e-f264792e3240",
    "team": null,
    "checkInDate": null,
    "groupId": null,
    "skillLevel": null
  }
"""

@dataclass
class Participant:
    participant: str
    # TODO add more fields 

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        participant = data.get("participant")

        if participant is None:
            raise ValueError("Invalid participant data: missing 'participant'")

        return cls(participant)

@dataclass
class TeamPlayer:
    account_id: str

@dataclass
class Team:
    id: str
    name: str
    players: List[TeamPlayer]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        id = data.get("Id")
        name = data.get("Name")
        players = [TeamPlayer(account_id=player.get("AccountId")) for player in data.get("Players", [])]

        if id is None or name is None:
            raise ValueError("Invalid team data: missing 'Id' or 'Name'")

        return cls(id=id, name=name, players=players)