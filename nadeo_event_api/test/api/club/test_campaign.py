import os
import pytest
from src.nadeo_event_api.environment import MY_CLUB
from src.nadeo_event_api.api.club.campaign import Campaign
from src.nadeo_event_api.api.structure.maps import PlaylistMap
import unittest


class TestCampaign(unittest.TestCase):
    @pytest.mark.integration
    def test_get_campaign_map_playlist(self):
        test_club_id = 69352  # Auto Events Staging
        test_campaign_id = 55190  # Test Campaign

        test_campaign = Campaign(test_club_id, test_campaign_id)

        expected = [
            PlaylistMap("UGGBkWkQrVhRN_A21iPrC7N1vzl", 0),
            PlaylistMap("rWQJGIHxjigGa0yB8KiNmwBLMCe", 1),
            PlaylistMap("55swQ8IfqZCkloLBFnMDQjOGRii", 2),
            PlaylistMap("qixNDvlk9TPcStquClVVoSftNwj", 3),
            PlaylistMap("fdArnftBTYFWzhqfiGIgjjl3XJ3", 4),
        ]

        self.assertEqual(expected, test_campaign._playlist)
