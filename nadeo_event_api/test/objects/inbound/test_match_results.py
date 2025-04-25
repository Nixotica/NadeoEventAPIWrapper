import unittest

from src.nadeo_event_api.objects.inbound.match_results import MatchResults, RankedParticipant, RankedTeam


class TestMatchResults(unittest.TestCase):
    def test_get_position(self):
        ranked_participant_1 = RankedParticipant(
            "tm_acc_1",
            rank=1,
            score=1,
            zone=None,
            team=None,
        )
        ranked_participant_2 = RankedParticipant(
            "tm_acc_2",
            rank=2,
            score=0,
            zone=None,
            team=None,
        )

        solo_match_results = MatchResults(
            match_live_id="test_match_1",
            round_position=0,
            results=[ranked_participant_1, ranked_participant_2],
            teams=[]
        )

        self.assertEqual(solo_match_results.get_rank("tm_acc_1"), 1)
        self.assertEqual(solo_match_results.get_rank("tm_acc_2"), 2)
        self.assertEqual(solo_match_results.get_rank("tm_acc_3"), None)

        ranked_participant_3 = RankedParticipant(
            "tm_acc_3",
            rank=3,
            score=0,
            zone=None,
            team="Blue",
        )
        ranked_participant_4 = RankedParticipant(
            "tm_acc_4",
            rank=4,
            score=0,
            zone=None,
            team="Blue",
        )
        ranked_participant_5 = RankedParticipant(
            "tm_acc_5",
            rank=5,
            score=0,
            zone=None,
            team="Red",
        )
        ranked_participant_6 = RankedParticipant(
            "tm_acc_6",
            rank=6,
            score=0,
            zone=None,
            team="Red",
        )
        ranked_team_blue = RankedTeam(
            position=0,
            team="Blue",
            rank=1,
            score=1,
        )
        ranked_team_red = RankedTeam(
            position=1,
            team="Red",
            rank=2,
            score=0,
        )

        team_match_results = MatchResults(
            match_live_id="test_match_2",
            round_position=0,
            results=[ranked_participant_3, ranked_participant_4, ranked_participant_5, ranked_participant_6],
            teams=[ranked_team_blue, ranked_team_red]
        )

        self.assertEqual(team_match_results.get_rank("tm_acc_3"), 1)
        self.assertEqual(team_match_results.get_rank("tm_acc_4"), 1)
        self.assertEqual(team_match_results.get_rank("tm_acc_5"), 2)
        self.assertEqual(team_match_results.get_rank("tm_acc_6"), 2)