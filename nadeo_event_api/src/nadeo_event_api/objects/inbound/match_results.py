from dataclasses import dataclass
from typing import Any, Dict, List, Optional

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

    def get_rank(self, participant_id: str) -> Optional[int]:
        """Returns a player's rank for a match, defaulting to their team rank if it was a teams match.

        Args:
            participant_id (str): The player's tm account ID.

        Returns:
            Optional[int]: The player's rank, if they had results in the match. 
        """
        # If not teams match, get player's individual rank
        if self.teams == []:        
            for result in self.results:
                if result.participant == participant_id:
                    return result.rank
                
        # If teams match, get player's team's rank
        else: 
            player_team = None
            for result in self.results:
                if result.participant == participant_id:
                    player_team = result.team

            if player_team is None:
                return None
            
            for team in self.teams:
                if team.team == player_team:
                    return team.rank

        return None