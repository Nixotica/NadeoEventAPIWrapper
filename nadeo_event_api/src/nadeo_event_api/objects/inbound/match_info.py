from dataclasses import dataclass
from typing import Any, Dict, List
from ...api.structure.enums import ParticipantType, ScriptType


@dataclass
class PublicConfig:
    script: ScriptType
    maps: List[str] | None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        script = data.get("script")
        maps = data.get("maps")

        return cls(
            script=ScriptType(script),
            maps=maps,
        )


""" 
Example:

{'id': 9874935, 'liveId': 'LID-MTCH-giobsduto0ompa1', 'name': 'BetterMMTest - Better Match - 1', 'startDate': 1725514047, 'endDate': 1725517647, 'status': 'COMPLETED', 'participantType': 'player', 'joinLink': None, 'serverStatus': 'DELETED', 'manialink': '', 'publicConfig': None, 'mediaUrl': ''}

"""


@dataclass
class MatchInfo:
    id: int | None
    live_id: str | None
    name: str | None
    start_date: int | None
    end_date: int | None
    status: str | None  # TODO - enumerate
    participant_type: str | None
    join_link: str | None
    server_status: str | None  # TODO - enumerate
    manialink: str | None
    public_config: PublicConfig | None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        id = data.get("id")
        live_id = data.get("liveId")
        name = data.get("name")
        start_date = data.get("startDate")
        end_date = data.get("endDate")
        status = data.get("status")
        participant_type = data.get("participantType")
        join_link = data.get("joinLink")
        server_status = data.get("serverStatus")
        manialink = data.get("manialink")
        public_config = data.get("publicConfig")

        return cls(
            id=id,
            live_id=live_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
            status=status,
            participant_type=participant_type,
            join_link=join_link,
            server_status=server_status,
            manialink=manialink,
            public_config=PublicConfig.from_dict(public_config),  # type: ignore
        )
