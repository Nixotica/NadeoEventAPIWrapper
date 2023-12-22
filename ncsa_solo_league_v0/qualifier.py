import datetime
from datetime import datetime, timedelta
from typing import List

# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
event_api_pkg = os.path.join(Path(__file__).resolve().parent.parent, "nadeo_event_api/src/")
sys.path.append(str(event_api_pkg))

from api.club.campaign import Campaign
from api.structure.maps import Map
from api.structure.round.qualifier import Qualifier
from constants import CLUB_AUTO_EVENTS_STAGING


def get_qualifier(
    start_date: datetime,
    map_pool: List[Map],
    warmup_sec: int,
    minutes_per_map: int,
) -> Qualifier:
    return Qualifier(
        name="Time Attack Qualifier",
        start_date=start_date,
        end_date=start_date + timedelta(minutes=len(map_pool) * (minutes_per_map + warmup_sec + 20)),
        # TODO
    )

### NOTE fill these out as appropriate each time the script is run! You shouldn't need to modify anything else! ###
event_name = "Test Solo League Event"
club_id = CLUB_AUTO_EVENTS_STAGING
campaign_id = 57253 # "Test Solo League"

now = datetime.utcnow()
registration_start_date = now + timedelta(minutes=1)
qualifier_start_date = now + timedelta(minutes=3)
qualifier_minutes_per_map = 5
### NOTE END ###

# Get the map pool
campaign_playlist = Campaign(club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist]

# Create qualifier
qualifier = get_qualifier(qualifier_start_date, map_pool, qualifier_minutes_per_map)