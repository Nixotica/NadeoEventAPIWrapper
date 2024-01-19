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
from nadeo_event_api.api.structure.settings.script_settings import TMWTScriptSettings


# Event info
event_name = "TMWTExample"
club_id = 69352 # "Auto Events Staging"
campaign_id = 57253  # "Test Solo League"

#
team_a = [
    "dadbaf28-e7b5-429b-bf37-8c8c1419fcf4",  # That_Ski_Freak
    "bd45204c-80f1-4809-b983-38b3f0ffc1ef",  # WirtualTM
]
team_b = [
    "b981e0b1-2d6a-4470-9b52-c1f6b0b1d0a6",  # longi.tm
    "2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
]

now = datetime.utcnow()
match_start = now + timedelta(minutes=2)

# Get the map pool
campaign_playlist = Campaign(club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist]

# Create the event
event = Event(
    name=event_name,
    club_id=club_id,
    rounds=[Round(
        name="Round 1",
        start_date=match_start,
        end_date=match_start + timedelta(hours=1),
        matches=[Match(
            spots=[TeamMatchSpot(1), TeamMatchSpot(2)],
        )],
        config=RoundConfig(
            map_pool=map_pool,
            script=ScriptType.TMWT_TEAMS,
            max_players=4,
            script_settings=TMWTScriptSettings(
                match_points_limit=4,
            ),
            plugin_settings=TMWTPluginSettings(
                ready_minimum_team_size=1,
            ),
        ),
    )],
    participant_type=ParticipantType.TEAM,
)
event.post()

# Add teams
event.add_team("team_a", team_a, 1)
event.add_team("team_b", team_b, 2)
