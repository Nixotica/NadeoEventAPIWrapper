# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
import os
from pathlib import Path
import sys


event_api_pkg = os.path.join(
    Path(__file__).resolve().parent.parent, "nadeo_event_api/src/"
)
sys.path.append(str(event_api_pkg))

from nadeo_event_api.api.event_api import get_matches_for_round, get_match_results

round_id = 58043
match = get_matches_for_round(round_id, 1, 0)[0]
match_results = get_match_results(match.id, 4, 0)

print(match_results)