import datetime
from datetime import UTC, datetime, timedelta, tzinfo
import os
from pathlib import Path
import sys
from typing import Dict, List

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
    LeaderboardType,
    ScriptType,
)
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.match_spot import SeedMatchSpot
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.api.structure.settings.script_settings import (
    CupSpecialScriptSettings,
)
from nadeo_event_api.api.structure.settings.plugin_settings import ClassicPluginSettings
from nadeo_event_api.constants import CLUB_AUTO_EVENTS_STAGING
from nadeo_event_api.api.structure.round.match import Match


def get_player_combinations(players: List[str]) -> List[List[Dict[int, str]]]:
    """
    Gets a list of player combinations as 5 matches where each player
    plays in exactly one match with every other player once. Returned as
    [rounds x matches] array of dicts mapping Seed (1-indexed) to player UUIDs.
    """

    players.insert(0, "spacer")
    return [
        [
            {1: players[1], 8: players[8], 9: players[9], 16: players[16]},
            {2: players[2], 7: players[7], 10: players[10], 15: players[15]},
            {3: players[3], 6: players[6], 11: players[11], 14: players[14]},
            {4: players[4], 5: players[5], 12: players[12], 13: players[13]},
        ],
        [
            {1: players[1], 2: players[2], 6: players[6], 12: players[12]},
            {8: players[8], 13: players[13], 14: players[14], 15: players[15]},
            {3: players[3], 4: players[4], 7: players[7], 9: players[9]},
            {5: players[5], 10: players[10], 11: players[11], 16: players[16]},
        ],
        [
            {1: players[1], 3: players[3], 5: players[5], 15: players[15]},
            {6: players[6], 9: players[9], 10: players[10], 13: players[13]},
            {7: players[7], 12: players[12], 14: players[14], 16: players[16]},
            {2: players[2], 4: players[4], 8: players[8], 11: players[11]},
        ],
        [
            {1: players[1], 4: players[4], 10: players[10], 14: players[14]},
            {5: players[5], 6: players[6], 7: players[7], 8: players[8]},
            {9: players[9], 11: players[11], 12: players[12], 15: players[15]},
            {2: players[2], 3: players[3], 13: players[13], 16: players[16]},
        ],
        [
            {1: players[1], 7: players[7], 11: players[11], 13: players[13]},
            {3: players[3], 8: players[8], 10: players[10], 12: players[12]},
            {2: players[2], 5: players[5], 9: players[9], 14: players[14]},
            {4: players[4], 6: players[6], 15: players[15], 16: players[16]},
        ],
    ]


def get_round(
    start_date: datetime,
    round_name: str,
    matches: List[Dict[int, str]],
    map_pool: List[Map],
) -> Round:
    return Round(
        name=round_name,
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            Match(spots=[SeedMatchSpot(seed) for seed in match.keys()])
            for match in matches
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=RoundConfig(
            map_pool=map_pool,
            script=ScriptType.CUP_LONG,
            max_players=4,
            script_settings=CupSpecialScriptSettings(
                warmup_number=1,
                warmup_duration=60,
                points_repartition="10,5,3,0",
                cup_points_limit=30,
                match_points_limit=2,
                number_of_winners=3,
                finish_timeout=10,
            ),
            plugin_settings=ClassicPluginSettings(
                pick_ban_start_auto=True,
                pick_ban_order="b:0,b:1,p:0,p:1,p:2,p:3,b:3,b:4,p:0,p:1,p:r",
                auto_start_mode=AutoStartMode.DISABLED,
                use_auto_ready=False,
            ),
        ),
    )


### NOTE fill these out as appropriate each time the script is run! You shouldn't need to modify anything else! ###
event_name = "TestSoloLeague"
club_id = CLUB_AUTO_EVENTS_STAGING
campaign_id = 57253  # "Test Solo League"

# This MUST be 16 players in order of seed (1-16)
players = [
    "dadbaf28-e7b5-429b-bf37-8c8c1419fcf4",  # That_Ski_Freak
    "bd45204c-80f1-4809-b983-38b3f0ffc1ef",  # WirtualTM
    "6e3bf3f9-7dcb-47d4-bdae-037ab66628f2",  # RandomizeTM
    "ef39801d-e749-4068-821a-8670602f2f24",  # xavier_b
    "5a59227d-2cfa-42de-851c-a20eb81f0626",  # Llamasticot
    "2232c721-f215-4036-b28b-772eee46632c",  # Hylis
    "7cd60a75-609a-4e64-b286-16f329878249",  # Tona.
    "5e7b0c82-263b-41d5-8fa4-98d36ad4d57c",  # lulurouge2
    "9b11ca6f-a7b6-437f-9b32-7b9a204543d2",  # gou1
    "4ef2a675-3885-466a-bd13-032bba5fb2bc",  # JesterMeijin
    "54e4dda4-522d-496f-8a8b-fe0d0b5a2a8f",  # Braxilior
    "0060a0c1-2e62-41e7-9db7-c86236af3ac4",  # magnetik.org
    "a76653e1-998a-4c53-8a91-0a396e15bfb5",  # MrDarrek
    "39be7ebf-2517-4c59-8091-53daec796e89",  # Ubi-Alinoa
    "b981e0b1-2d6a-4470-9b52-c1f6b0b1d0a6",  # longi.tm
    "2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
]

# now = datetime.utcnow()
# Each step takes approximately 2 hours
step_1_start = datetime(
    year=2024,
    month=3,
    day=2,
    hour=20,
    tzinfo=UTC,
)  # March 2 2024 @ 12:00pm Pacific
step_2_start = step_1_start + timedelta(hours=2)  # 2:00pm
step_3_start = step_1_start + timedelta(hours=4)  # 4:00pm
step_4_start = step_1_start + timedelta(days=7)  # March 9 2024 @ 12:00pm Pacific
step_5_start = step_4_start + timedelta(hours=2)  # 2:00pm
### NOTE END ###

# Get the map pool
campaign_playlist = Campaign(club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist]

# Get the rounds (5) and matches (4) of players (16 / 4)
rounds_and_matches = get_player_combinations(players)

round_1 = get_round(step_1_start, "Step 1", rounds_and_matches[0], map_pool)
round_2 = get_round(step_2_start, "Step 2", rounds_and_matches[1], map_pool)
round_3 = get_round(step_3_start, "Step 3", rounds_and_matches[2], map_pool)
round_4 = get_round(step_4_start, "Step 4", rounds_and_matches[3], map_pool)
round_5 = get_round(step_5_start, "Step 5", rounds_and_matches[4], map_pool)

# Create and post the event
event = Event(
    name=event_name,
    club_id=club_id,
    rounds=[round_1, round_2, round_3, round_4, round_5],
)
event.post()

# Add the players to the event
for player_idx in range(len(players)):
    event.add_participant(players[player_idx], player_idx + 1)
