from datetime import datetime, timedelta
import os
import pytest
import unittest
import json

from nadeo_event_api.environment import MY_CLUB
from ..utils_for_test import are_json_structures_equal
from src.nadeo_event_api.api.structure.round.qualifier import Qualifier, QualifierConfig
from src.nadeo_event_api.api.structure.maps import Map
from src.nadeo_event_api.api.structure.enums import LeaderboardType, ScriptType
from src.nadeo_event_api.api.structure.round.match_spot import SeedMatchSpot
from src.nadeo_event_api.api.structure.round.match import Match
from src.nadeo_event_api.api.structure.round.round import Round, RoundConfig
from src.nadeo_event_api.api.structure.event import Event


class TestEvent(unittest.TestCase):
    def test_basic_event_as_jsonable_dict(self):
        with open("test/api/structure/resources/basic_event.json") as f:
            expected: dict = json.load(f)
        actual = Event(
            name="my_event",
            club_id=123,
            description="my_description",
            registration_start_date=datetime(2023, 11, 3, 20, 45),
            registration_end_date=datetime(2023, 11, 3, 20, 55),
            rounds=[
                Round(
                    name="round_1",
                    start_date=datetime(2023, 11, 3, 21, 5),
                    end_date=datetime(2023, 11, 3, 21, 15),
                    matches=[
                        Match(
                            spots=[
                                SeedMatchSpot(
                                    seed=1,
                                ),
                                SeedMatchSpot(
                                    seed=2,
                                ),
                            ],
                        ),
                    ],
                    config=RoundConfig(
                        map_pool=[
                            Map("round_map"),
                        ],
                        script=ScriptType.CUP,
                        max_players=32,
                    ),
                    qualifier=Qualifier(
                        name="qualifier_1",
                        start_date=datetime(2023, 11, 3, 20, 55),
                        end_date=datetime(2023, 11, 3, 21, 5),
                        leaderboard_type=LeaderboardType.SUM,
                        config=QualifierConfig(
                            map_pool=[Map("quali_map")],
                            script=ScriptType.TIME_ATTACK,
                            max_players=64,
                        ),
                    ),
                ),
            ],
        )._as_jsonable_dict()

        self.assertTrue(are_json_structures_equal(expected, actual))

    @pytest.mark.integration
    def test_post_and_delete_event(self):
        now = datetime.utcnow()
        event = Event(
            name="my_event",
            club_id=os.getenv(MY_CLUB),  # type: ignore
            rounds=[
                Round(
                    name="round_1",
                    start_date=now + timedelta(minutes=50),
                    end_date=now + timedelta(minutes=80),
                    matches=[
                        Match(
                            spots=[
                                SeedMatchSpot(
                                    seed=1,
                                ),
                                SeedMatchSpot(
                                    seed=2,
                                ),
                            ],
                        ),
                    ],
                    config=RoundConfig(
                        map_pool=[
                            Map("_jTSBKAuePtwJ2tUz8UZx25rYzl"),
                        ],
                        script=ScriptType.CUP,
                        max_players=32,
                    ),
                    qualifier=Qualifier(
                        name="qualifier_1",
                        start_date=now + timedelta(minutes=10),
                        end_date=now + timedelta(minutes=40),
                        leaderboard_type=LeaderboardType.SUM,
                        config=QualifierConfig(
                            map_pool=[Map("_jTSBKAuePtwJ2tUz8UZx25rYzl")],
                            script=ScriptType.TIME_ATTACK,
                            max_players=64,
                        ),
                    ),
                ),
            ],
        )
        event.post()
        self.assertIsNotNone(event._registered_id)
        event.add_logo("https://www.trackmania.com/build/images/Flags/GBR.1ef3a1eb.png")
        self.assertIsNotNone(event._registered_logo_url)
        event.delete()
        self.assertIsNone(event._registered_id)
