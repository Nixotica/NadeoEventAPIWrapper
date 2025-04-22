CREATE_COMP_URL = "https://meet.trackmania.nadeo.club/api/competitions/web/create"

# https://webservices.openplanet.dev/meet/competitions/leaderboard
GET_EVENT_LEADERBOARD_URL_FMT = "https://meet.trackmania.nadeo.club/api/competitions/{0}/leaderboard?length={1}&offset={2}"

# https://webservices.openplanet.dev/meet/competition-matches/results
GET_MATCH_RESULTS_URL_FMT = (
    "https://meet.trackmania.nadeo.club/api/matches/{0}/results?length={1}&offset={2}"
)

# https://webservices.openplanet.dev/meet/matches/match
GET_MATCH_INFO_URL_FMT = "https://meet.trackmania.nadeo.club/api/matches/{0}"

# https://webservices.openplanet.dev/meet/competition-matches/matches-for-round
GET_MATCHES_FOR_ROUND_URL_FMT = (
    "https://meet.trackmania.nadeo.club/api/rounds/{0}/matches?length={1}&offset={2}"
)

# https://webservices.openplanet.dev/meet/competitions/rounds
GET_ROUNDS_FOR_EVENT_URL_FMT = (
    "https://meet.trackmania.nadeo.club/api/competitions/{0}/rounds"
)

# https://webservices.openplanet.dev/meet/competitions/participants
GET_EVENT_PARTICIPANTS_URL_FMT = (
    "https://meet.trackmania.nadeo.club/api/competitions/{0}/participants?length={1}&offset={2}"
)

# https://webservices.openplanet.dev/meet/competitions/teams
GET_EVENT_TEAMS_URL_FMT = (
    "https://meet.trackmania.nadeo.club/api/competitions/{0}/mode-teams"
)

PASTEBIN_POST_URL = "https://pastebin.com/api/api_post.php"

PASTES_IO_LOGIN_URL = "http://pastesio.com/api/login"
PASTES_IO_CREATE_URL = "http://pastesio.com/api/paste/create"

PASTEFY_SKIFF_CREATE_URL = "https://pastes.skiff.dev/api/v2/paste"
PASTEFY_SKIFF_RAW_URL_FMT = "https://pastes.skiff.dev/{0}/raw"