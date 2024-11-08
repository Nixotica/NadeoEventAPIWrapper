from dataclasses import dataclass
from typing import Any, Dict, List

"""
Example: 

{'participant': '12ea0824-1698-4c61-ba1f-c2eb73a97477', 'rank': None, 'score': None, 'zone': 'World', 'team': None}
"""


@dataclass
class RankedParticipant:
    participant: str
    rank: int | None
    score: int | None
    zone: str | None
    team: str | None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        participant = data.get("participant")
        rank = data.get("rank")
        score = data.get("score")
        zone = data.get("zone")
        team = data.get("team")

        return cls(participant, rank, score, zone, team)  # type: ignore


"""
Example: 

{'position': 1, 'team': 'Red', 'rank': 2, 'score': 0}
"""


@dataclass
class RankedTeam:
    position: int
    team: str
    rank: int
    score: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        position = data.get("position")
        team = data.get("team")
        rank = data.get("rank")
        score = data.get("score")

        return cls(position, team, rank, score)  # type: ignore


"""
Example: 

{'matchLiveId': 'LID-MTCH-bs5s12wftrrdqjp', 'roundPosition': 0, 'results': [RankedParticpant], 'scoreUnit': 'point', 'teams': []}
"""


@dataclass
class MatchResults:
    match_live_id: str
    round_position: int
    results: List[RankedParticipant]
    teams: List[RankedTeam]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        match_live_id = data.get("matchLiveId")
        round_position = data.get("roundPosition")
        results = [RankedParticipant.from_dict(result) for result in data.get("results", [])]
        teams = [RankedTeam.from_dict(team) for team in data.get("teams", [])]  

        return cls(match_live_id, round_position, results, teams)  # type: ignore
