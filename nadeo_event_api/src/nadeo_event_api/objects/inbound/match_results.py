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

        return cls(participant, rank, score, zone, team) # type: ignore



"""
Example: 

{'matchLiveId': 'LID-MTCH-bs5s12wftrrdqjp', 'roundPosition': 0, 'results': [RankedParticpant], 'scoreUnit': 'point', 'teams': []}
"""


@dataclass
class MatchResults:
    match_live_id: str
    round_position: int
    results: List[RankedParticipant]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        match_live_id = data.get("matchLiveId")
        round_position = data.get("roundPosition")
        results = [RankedParticipant.from_dict(result) for result in data.get("results")] # type: ignore

        return cls(match_live_id, round_position, results) # type: ignore