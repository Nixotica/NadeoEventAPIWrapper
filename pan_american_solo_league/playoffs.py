from datetime import datetime, timedelta
import os
from pathlib import Path
import sys
from typing import List

# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
event_api_pkg = os.path.join(
    Path(__file__).resolve().parent.parent, "nadeo_event_api/src/"
)
sys.path.append(str(event_api_pkg))

from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.club.campaign import Campaign
from nadeo_event_api.api.structure.enums import (
    AutoStartMode,
    ScriptType,
)
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import (
    MatchParticipantMatchSpot,
    SeedMatchSpot,
)
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.api.structure.settings.script_settings import (
    CupSpecialScriptSettings,
)
from nadeo_event_api.api.structure.settings.plugin_settings import ClassicPluginSettings


def get_round(
    start_date: datetime,
    round_name: str,
    map_pool: List[Map],
    first_seed: int = None,
    second_seed: int = None,
    prev_first_seed_round: int = None,
    prev_second_seed_round: int = None,
) -> Round:
    return Round(
        name=round_name,
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[Match(spots=[SeedMatchSpot(first_seed), SeedMatchSpot(second_seed)])]
        if first_seed is not None
        else [
            Match(
                spots=[
                    MatchParticipantMatchSpot(prev_first_seed_round, 0, 1),
                    MatchParticipantMatchSpot(prev_second_seed_round, 0, 1),
                ]
            )
        ],
        config=RoundConfig(
            map_pool=map_pool,
            script=ScriptType.CUP_LONG,
            max_players=2,
            script_settings=CupSpecialScriptSettings(
                points_repartition="1,0",
                number_of_winners=1,
                warmup_duration=60,
                match_points_limit=4,
                cup_points_limit=4,
            ),
            plugin_settings=ClassicPluginSettings(
                pick_ban_start_auto=True,
                pick_ban_order="b:1,b:0,p:0,p:1,p:0,p:1,p:0,p:1,p:0,p:1,p:r",
                auto_start_mode=AutoStartMode.DISABLED,
                use_auto_ready=False,
            ),
        ),
    )


### NOTE fill these out as appropriate each time the script is run! You shouldn't need to modify anything else! ###
event_name = "PASL Playoffs"
club_id = 69352 # "Auto Events Staging"
campaign_id = 57253  # "Test Solo League"

# This MUST be 8 players in order of seed (1-8)
players = [
    "dadbaf28-e7b5-429b-bf37-8c8c1419fcf4",  # That_Ski_Freak
    "bd45204c-80f1-4809-b983-38b3f0ffc1ef",  # WirtualTM
    "6e3bf3f9-7dcb-47d4-bdae-037ab66628f2",  # RandomizeTM
    "ef39801d-e749-4068-821a-8670602f2f24",  # xavier_b
    "a76653e1-998a-4c53-8a91-0a396e15bfb5",  # MrDarrek
    "39be7ebf-2517-4c59-8091-53daec796e89",  # Ubi-Alinoa
    "b981e0b1-2d6a-4470-9b52-c1f6b0b1d0a6",  # longi.tm
    "2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
]

now = datetime.utcnow()
quarter_1_start = now + timedelta(minutes=1)
quarter_2_start = now + timedelta(hours=10)
quarter_3_start = now + timedelta(hours=15)
quarter_4_start = now + timedelta(hours=20)
semi_1_start = now + timedelta(hours=25)
semi_2_start = now + timedelta(hours=30)
grand_start = now + timedelta(hours=35)
### NOTE END ###

# Get the map pool
campaign_playlist = Campaign(club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist]

# Get all rounds, one match per round
quarter_1 = get_round(
    start_date=quarter_1_start,
    round_name="Quarter 1",
    map_pool=map_pool,
    first_seed=1,
    second_seed=8,
)
quarter_2 = get_round(
    start_date=quarter_2_start,
    round_name="Quarter 2",
    map_pool=map_pool,
    first_seed=2,
    second_seed=7,
)
quarter_3 = get_round(
    start_date=quarter_3_start,
    round_name="Quarter 3",
    map_pool=map_pool,
    first_seed=3,
    second_seed=6,
)
quarter_4 = get_round(
    start_date=quarter_4_start,
    round_name="Quarter 4",
    map_pool=map_pool,
    first_seed=4,
    second_seed=5,
)
semi_1 = get_round(
    start_date=semi_1_start,
    round_name="Semi 1",
    map_pool=map_pool,
    prev_first_seed_round=0,  # Quarter 1
    prev_second_seed_round=3,  # Quarter 4
)
semi_2 = get_round(
    start_date=semi_2_start,
    round_name="Semi 2",
    map_pool=map_pool,
    prev_first_seed_round=1,  # Quarter 2
    prev_second_seed_round=2,  # Quarter 3
)
grand = get_round(
    start_date=grand_start,
    round_name="Grand Final",
    map_pool=map_pool,
    prev_first_seed_round=4,  # Semi 1
    prev_second_seed_round=5,  # Semi 2
)

# Create and post the event
event = Event(
    name=event_name,
    club_id=club_id,
    rounds=[quarter_1, quarter_2, quarter_3, quarter_4, semi_1, semi_2, grand],
)
event.post()

# Add the players to the event
for player_idx in range(len(players)):
    event.add_participant(players[player_idx], player_idx + 1)
