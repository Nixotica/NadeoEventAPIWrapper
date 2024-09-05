from dataclasses import dataclass
from typing import Any, Dict

from ...api.structure.enums import LeaderboardType

"""
Example:

{'id': 53031, 'position': 0, 'name': 'Better Match', 'startDate': 1725506356, 'endDate': 1725509956, 'lockDate': None, 'status': 'HAS_MATCHES', 'isLocked': False, 'autoNeedsMatches': True, 'matchScoreDirection': 'DESC', 'leaderboardComputeType': 'BRACKET', 'teamLeaderboardComputeType': 'TEAM_SCORE', 'deletedOn': None, 'nbMatches': 1, 'qualifierChallengeId': None, 'trainingChallengeId': None}
"""


@dataclass
class Round:
    id: int
    position: int
    name: str
    start_date: int
    end_date: int
    lock_date: int | None
    status: str  # TODO - enum
    is_locked: bool
    auto_needs_matches: bool
    match_score_direction: str  # TODO - enum
    leaderboard_compute_type: LeaderboardType
    team_leadaerboard_compute_type: str  # TODO - enum
    deleted_on: int | None
    num_matches: int
    qualifier_challenge_id: int | None
    training_challenge_id: int | None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        id = data.get("id")
        position = data.get("position")
        name = data.get("name")
        start_date = data.get("startDate")
        end_date = data.get("endDate")
        lock_date = data.get("lockDate")
        status = data.get("status")
        is_locked = data.get("isLocked")
        auto_needs_matches = data.get("autoNeedsMatches")
        match_score_direction = data.get("matchScoreDirection")
        leaderboard_compute_type = data.get("leaderboardComputeType")
        team_leaderboard_compute_type = data.get("teamLeaderboardComputeType")
        deleted_on = data.get("deletedOn")
        num_matches = data.get("nbMatches")
        qualifier_challenge_id = data.get("qualifierChallengeId")
        training_challenge_id = data.get("trainingChallengeId")

        return cls(id, position, name, start_date, end_date, lock_date, status, is_locked, auto_needs_matches, match_score_direction, leaderboard_compute_type, team_leaderboard_compute_type, deleted_on, num_matches, qualifier_challenge_id, training_challenge_id)  # type: ignore
