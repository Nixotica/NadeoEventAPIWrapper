import datetime
from datetime import datetime, timedelta
import os
from pathlib import Path
import sys

# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
event_api_pkg = os.path.join(
    Path(__file__).resolve().parent.parent, "nadeo_event_api/src/"
)
sys.path.append(str(event_api_pkg))

from nadeo_event_api.api.club.campaign import Campaign
from nadeo_event_api.api.structure.enums import (
    ParticipantType,
    ScriptType,
)
from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import TeamMatchSpot
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.api.structure.settings.plugin_settings import TMWTPluginSettings
from nadeo_event_api.api.structure.settings.script_settings import TMWTScriptSettings, BaseScriptSettings


# Event info
event_name = "finalfinal"
match_club_id = 69352  # "Auto Events Staging"
campaign_club_id = 383 # TMWT
campaign_id = 74274  # "TMWT Fall 2024"

# Create teams of two by UID
team_a = [
    "2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
    "6e3bf3f9-7dcb-47d4-bdae-037ab66628f2",  # Randomize
]
team_b = [
    "ec0269d5-2d19-41eb-a931-01b8a11c2784",  # Random
    "df9448f1-a8d5-4682-9003-1c2777c62b91",  # alxshaer
]

now = datetime.utcnow()
match_start = now + timedelta(minutes=1)

# Get the map pool
campaign_playlist = Campaign(campaign_club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist] # type: ignore

# Create the event
event = Event(
    name=event_name,
    club_id=match_club_id,
    rounds=[
        Round(
            name="Round 1",
            start_date=match_start,
            end_date=match_start + timedelta(hours=1),
            matches=[
                Match(
                    spots=[TeamMatchSpot(1), TeamMatchSpot(2)],
                )
            ],
            config=RoundConfig(
                map_pool=[map_pool[3]],
                script=ScriptType.TMWT_TEAMS,
                max_players=4,
                script_settings=TMWTScriptSettings(
                    base_script_settings=BaseScriptSettings(
                        warmup_number=1,
                        warmup_duration=60,
                    ),
                    teams_url="https://pastebin.com/raw/62NPyvWu",  # (Nixotica, Randomize) vs (alxshaer, Random)
                    match_points_limit=1,
                    match_info="Fuck me Randomize"
                ),
                plugin_settings=TMWTPluginSettings(
                    ready_minimum_team_size=1,
                    pick_ban_start_auto=False,
                    pick_ban_order="",
                ),
            ),
        )
    ],
    participant_type=ParticipantType.TEAM,
)
event.post()

# Add teams
event.add_team("Blu", team_a, 1)
event.add_team("Red", team_b, 2)
