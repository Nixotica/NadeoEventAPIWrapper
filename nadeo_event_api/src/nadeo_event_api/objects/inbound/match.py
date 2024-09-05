from dataclasses import dataclass
from typing import Any, Dict, List

"""
Example:

{'id': 97677, 'name': 'BetterMMTest - Better Match - 1', 'clubMatchLiveId': 'LID-MTCH-bs5s12wftrrdqjp', 'position': 0, 'isCompleted': False, 'tags': [], 'deletedOn': None}
"""


@dataclass
class Match:
    id: int
    name: str
    club_match_live_id: str
    position: int
    is_completed: bool
    tags: List[str]
    deleted_on: int | None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        id = data.get("id")
        name = data.get("name")
        club_match_live_id = data.get("clubMatchLiveId")
        position = data.get("position")
        is_completed = data.get("isCompleted")
        tags = data.get("tags")
        deleted_on = data.get("deletedOn")

        return cls(id, name, club_match_live_id, position, is_completed, tags, deleted_on) # type: ignore