from datetime import datetime, timedelta
import json
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

from nadeo_event_api.api.structure.settings.plugin_settings import ClassicPluginSettings
from nadeo_event_api.api.structure.settings.script_settings import (
    CupSpecialScriptSettings,
)
from nadeo_event_api.api.structure.round.qualifier import Qualifier, QualifierConfig
from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.club.campaign import Campaign
from nadeo_event_api.api.structure.enums import LeaderboardType, ScriptType
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import (
    MatchParticipantMatchSpot,
    QualificationMatchSpot,
)
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.constants import CLUB_AUTO_EVENTS_STAGING


def get_round_config(
    map_pool: List[Map],
) -> RoundConfig:
    return RoundConfig(
        map_pool=map_pool,
        script=ScriptType.CUP_LONG,
        max_players=4,
        script_settings=CupSpecialScriptSettings(
            points_repartition="1,0,0,0",
            ko_checkpoint_number=0,
            number_of_winners=2,
            warmup_duration=60,
            match_points_limit=2,
            cup_points_limit=4,
        ),
        plugin_settings=ClassicPluginSettings(
            pick_ban_start_auto=True,
            pick_ban_order="b:0,p:0,p:1,p:2,p:3,b:3,p:0,p:1,p:2",
        ),
    )


def get_match_from_prev_round(
    prev_round: int,
    prev_first_seed_match: int,
    prev_first_seed_rank: int,
    prev_second_seed_match: int,
    prev_second_seed_rank: int,
    prev_third_seed_match: int,
    prev_third_seed_rank: int,
    prev_fourth_seed_match: int,
    prev_fourth_seed_rank: int,
) -> Match:
    return Match(
        spots=[
            MatchParticipantMatchSpot(
                prev_round, prev_first_seed_match, prev_first_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_round, prev_second_seed_match, prev_second_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_round, prev_third_seed_match, prev_third_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_round, prev_fourth_seed_match, prev_fourth_seed_rank
            ),
        ]
    )


def get_match_with_round(
    prev_first_seed_round: int,
    prev_first_seed_match: int,
    prev_first_seed_rank: int,
    prev_second_seed_round: int,
    prev_second_seed_match: int,
    prev_second_seed_rank: int,
    prev_third_seed_round: int,
    prev_third_seed_match: int,
    prev_third_seed_rank: int,
    prev_fourth_seed_round: int,
    prev_fourth_seed_match: int,
    prev_fourth_seed_rank: int,
) -> Match:
    return Match(
        spots=[
            MatchParticipantMatchSpot(
                prev_first_seed_round, prev_first_seed_match, prev_first_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_second_seed_round, prev_second_seed_match, prev_second_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_third_seed_round, prev_third_seed_match, prev_third_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_fourth_seed_round, prev_fourth_seed_match, prev_fourth_seed_rank
            ),
        ]
    )


def get_match_from_quali(
    first_seed: int,
    second_seed: int,
    third_seed: int,
    fourth_seed: int,
) -> Match:
    return Match(
        spots=[
            QualificationMatchSpot(0, first_seed),
            QualificationMatchSpot(0, second_seed),
            QualificationMatchSpot(0, third_seed),
            QualificationMatchSpot(0, fourth_seed),
        ]
    )


def get_gs_round_1(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="GS - Round 1",
        start_date=start_date + timedelta(minutes=35),
        end_date=start_date + timedelta(hours=1, minutes=35),
        matches=[
            get_match_from_quali(1, 17, 48, 64),
            get_match_from_quali(8, 24, 41, 57),
            get_match_from_quali(9, 25, 40, 56),
            get_match_from_quali(16, 32, 33, 49),
            get_match_from_quali(2, 18, 47, 63),
            get_match_from_quali(7, 23, 42, 58),
            get_match_from_quali(10, 26, 39, 55),
            get_match_from_quali(15, 31, 34, 50),
            get_match_from_quali(3, 19, 46, 62),
            get_match_from_quali(6, 22, 43, 59),
            get_match_from_quali(11, 27, 38, 54),
            get_match_from_quali(14, 30, 35, 51),
            get_match_from_quali(4, 20, 45, 61),
            get_match_from_quali(5, 21, 44, 60),
            get_match_from_quali(12, 28, 37, 53),
            get_match_from_quali(13, 29, 36, 52),
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=get_round_config(map_pool=map_pool),
        qualifier=Qualifier(
            name="Seeding Qualifier",
            start_date=start_date,
            end_date=start_date + timedelta(minutes=30),
            leaderboard_type=LeaderboardType.SUMSCORE,
            config=QualifierConfig(
                map_pool=map_pool,
                script=ScriptType.TIME_ATTACK,
            ),
        ),
    )


def get_gs_round_2(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="GS - Round 2",
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            get_match_from_prev_round(0, 0, 1, 1, 2, 2, 1, 3, 2),
            get_match_from_prev_round(0, 0, 2, 1, 1, 2, 2, 3, 1),
            get_match_from_prev_round(0, 0, 3, 1, 4, 2, 3, 3, 4),
            get_match_from_prev_round(0, 0, 4, 1, 3, 2, 4, 3, 3),
            get_match_from_prev_round(0, 4, 1, 5, 2, 6, 1, 7, 2),
            get_match_from_prev_round(0, 4, 2, 5, 1, 6, 2, 7, 1),
            get_match_from_prev_round(0, 4, 3, 5, 4, 6, 3, 7, 4),
            get_match_from_prev_round(0, 4, 4, 5, 3, 6, 4, 7, 3),
            get_match_from_prev_round(0, 8, 1, 9, 2, 10, 1, 11, 2),
            get_match_from_prev_round(0, 8, 2, 9, 1, 10, 2, 11, 1),
            get_match_from_prev_round(0, 8, 3, 9, 4, 10, 3, 11, 4),
            get_match_from_prev_round(0, 8, 4, 9, 3, 10, 4, 11, 3),
            get_match_from_prev_round(0, 12, 1, 13, 2, 14, 1, 15, 2),
            get_match_from_prev_round(0, 12, 2, 13, 1, 14, 2, 15, 1),
            get_match_from_prev_round(0, 12, 3, 13, 4, 14, 3, 15, 4),
            get_match_from_prev_round(0, 12, 4, 13, 3, 14, 4, 15, 3),
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=get_round_config(map_pool=map_pool),
    )


def get_gs_round_3(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="GS - Round 3",
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            get_match_from_prev_round(1, 0, 1, 0, 2, 1, 1, 1, 2),
            get_match_from_prev_round(1, 0, 3, 1, 4, 2, 1, 3, 2),
            get_match_from_prev_round(1, 0, 4, 1, 3, 2, 2, 3, 1),
            get_match_from_prev_round(1, 4, 1, 4, 2, 5, 1, 5, 2),
            get_match_from_prev_round(1, 4, 3, 5, 4, 6, 1, 7, 2),
            get_match_from_prev_round(1, 4, 4, 5, 3, 6, 2, 7, 1),
            get_match_from_prev_round(1, 8, 1, 8, 2, 9, 1, 9, 2),
            get_match_from_prev_round(1, 8, 3, 9, 4, 10, 1, 11, 2),
            get_match_from_prev_round(1, 8, 4, 9, 3, 10, 2, 11, 1),
            get_match_from_prev_round(1, 12, 1, 12, 2, 13, 1, 13, 2),
            get_match_from_prev_round(1, 12, 3, 13, 4, 14, 1, 15, 2),
            get_match_from_prev_round(1, 12, 4, 13, 3, 14, 2, 15, 1),
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=get_round_config(map_pool=map_pool),
    )


def get_gs_round_4(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="GS - Round 4",
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            get_match_from_prev_round(2, 1, 1, 1, 2, 2, 1, 2, 2),
            get_match_from_prev_round(2, 4, 1, 4, 2, 5, 1, 5, 2),
            get_match_from_prev_round(2, 7, 1, 7, 2, 8, 1, 8, 2),
            get_match_from_prev_round(2, 10, 1, 10, 2, 11, 1, 11, 2),
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=get_round_config(map_pool=map_pool),
    )


def get_swiss_round_1(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Swiss - Round 1",
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            get_match_with_round(2, 0, 3, 2, 9, 4, 3, 2, 1, 3, 1, 2),
            get_match_with_round(2, 3, 3, 2, 6, 4, 3, 3, 1, 3, 0, 2),
            get_match_with_round(2, 6, 3, 2, 3, 4, 3, 0, 1, 3, 3, 2),
            get_match_with_round(2, 9, 3, 2, 0, 4, 3, 1, 1, 3, 2, 2),
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=get_round_config(map_pool=map_pool),
    )


def get_swiss_round_2(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Swiss - Round 2",
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            get_match_with_round(4, 0, 1, 4, 1, 2, 4, 2, 2, 4, 3, 1),
            get_match_with_round(4, 0, 2, 4, 1, 1, 4, 2, 1, 4, 3, 2),
            get_match_with_round(4, 0, 3, 4, 1, 4, 4, 2, 4, 4, 3, 3),
            get_match_with_round(4, 0, 4, 4, 1, 3, 4, 2, 3, 4, 3, 4),
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=get_round_config(map_pool=map_pool),
    )


def get_swiss_round_3(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Swiss - Round 3",
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            get_match_with_round(5, 0, 3, 5, 1, 4, 5, 2, 1, 5, 3, 2),
            get_match_with_round(5, 0, 4, 5, 1, 3, 5, 2, 2, 5, 3, 1),
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=get_round_config(map_pool=map_pool),
    )


### NOTE fill these out as appropriate each time the script is run! You shouldn't need to modify anything else! ###
event_name = "TestPASLQuali"
club_id = CLUB_AUTO_EVENTS_STAGING
campaign_id = 57253  # Uses maps from a campaign

now = datetime.now()
gs_r1_quali_start = now + timedelta(minutes=5)
gs_r2_start = now + timedelta(hours=2)
gs_r3_start = now + timedelta(hours=4)
gs_r4_start = now + timedelta(hours=6)
swiss_r1_start = now + timedelta(hours=8)
swiss_r2_start = now + timedelta(hours=10)
swiss_r3_start = now + timedelta(hours=12)
### NOTE END ###

# Get the map pool
campaign_playlist = Campaign(club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist]

gs_r1 = get_gs_round_1(gs_r1_quali_start, map_pool)
gs_r2 = get_gs_round_2(gs_r2_start, map_pool)
gs_r3 = get_gs_round_3(gs_r3_start, map_pool)
gs_r4 = get_gs_round_4(gs_r4_start, map_pool)
swiss_r1 = get_swiss_round_1(swiss_r1_start, map_pool)
swiss_r2 = get_swiss_round_2(swiss_r2_start, map_pool)
swiss_r3 = get_swiss_round_3(swiss_r3_start, map_pool)

# Create and post the event
event = Event(
    name=event_name,
    club_id=club_id,
    rounds=[gs_r1, gs_r2, gs_r3, gs_r4, swiss_r1, swiss_r2, swiss_r3],
)
event.post()
