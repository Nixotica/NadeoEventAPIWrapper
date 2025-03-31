# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
import os
from pathlib import Path
import sys


event_api_pkg = os.path.join(
    Path(__file__).resolve().parent.parent, "nadeo_event_api/src/"
)
sys.path.append(str(event_api_pkg))

# from nadeo_event_api.api.event_api import get_matches_for_round, get_match_results

# round_id = 60229
# match = get_matches_for_round(round_id, 1, 0)[0]
# match_results = get_match_results(match.id, 4, 0)

# print(match_results)

# from nadeo_event_api.api.pastesio.pastesio_api import login, post_tmwt_2v2
# from nadeo_event_api.objects.outbound.pastebin.tmwt_2v2 import Tmwt2v2Paste, Tmwt2v2PasteTeam

# blue_team = Tmwt2v2PasteTeam(
#     team_id="blue",
#     team_name="Blue",
#     p1_tm_account_id="2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
#     p2_tm_account_id="6e3bf3f9-7dcb-47d4-bdae-037ab66628f2",  # Randomize
# )

# red_team = Tmwt2v2PasteTeam(
#     team_id="red",
#     team_name="Red",
#     p1_tm_account_id="c7818ba0-5e85-408e-a852-f658e8b90eec",  # Dummy
#     p2_tm_account_id="551dd1f5-2380-417d-98a5-8e2244f9287f",  # Revants
# )

# paste = Tmwt2v2Paste(
#     team_a=blue_team,
#     team_b=red_team,
# )

# token = login("User", "Pass")
# url = post_tmwt_2v2(paste, "test_paste", token) 
# print(url)

# from nadeo_event_api.api.event_api import get_event_teams, get_event_participants

# print(get_event_teams(24706))
# print(get_event_participants(24706, 4, 0))