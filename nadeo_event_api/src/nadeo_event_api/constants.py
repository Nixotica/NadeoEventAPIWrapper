CREATE_COMP_URL = "https://meet.trackmania.nadeo.club/api/competitions/web/create"

NADEO_AUTH_URL = (
    "https://prod.trackmania.core.nadeo.online/v2/authentication/token/basic"
)

NADEO_REFRESH_AUTH_URL = (
    "https://prod.trackmania.core.nadeo.online/v2/authentication/token/refresh"
)

CLUB_CAMPAIGN_URL_FMT = (
    "https://live-services.trackmania.nadeo.live/api/token/club/{0}/campaign/{1}"
)

DELETE_COMP_URL_FMT = "https://meet.trackmania.nadeo.club/api/competitions/{0}/delete"

ADD_PARTICIPANT_URL_FMT = (
    "https://meet.trackmania.nadeo.club/api/competitions/{0}/register"
)

ADD_TEAM_URL_FMT = "https://meet.trackmania.nadeo.club/api/competitions/{0}/teams"

ADD_LOGO_URL_FMT = "https://meet.trackmania.nadeo.club/api/competitions/{0}/upload/logo"

# https://webservices.openplanet.dev/meet/competitions/competition
GET_EVENT_URL_FMT = "https://meet.trackmania.nadeo.club/api/competitions/{0}"

GET_PARTICIPANTS_URL_FMT = "https://meet.trackmania.nadeo.club/api/competitions/{0}/participants?offset={1}&length={2}"

NADEO_DATE_FMT = "%Y-%m-%dT%H:%M:%S.000Z"
