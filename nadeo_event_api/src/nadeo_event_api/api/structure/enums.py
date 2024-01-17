from enum import Enum


class LeaderboardType(Enum):
    """
    The leaderboard type for a round. Determines how scoring the round works.
    """

    BRACKET = "BRACKET"
    SUMSCORE = "SUMSCORE"
    SUM = "SUM"

    # TODO support more leaderboard types


class ParticipantType(Enum):
    """
    The participant type for an event.
    """

    PLAYER = "PLAYER"
    TEAM = "TEAM"


class ScriptType(Enum):
    """
    The script type for a round. Determines the gamemode which will be played.
    """

    CUP = "TrackMania/TM_Cup_Online.Script.txt"
    ROUNDS = "TrackMania/TM_Rounds_Online.Script.txt"
    TIME_ATTACK = "TrackMania/TM_TimeAttack_Online.Script.txt"
    KNOCKOUT = "TrackMania/TM_Knockout_Online.Script.txt"
    """ Format used in COTD. """
    CUP_CLASSIC = "TrackMania/Legacy/TM_CupClassic_Online.Script.txt"
    """ Same as cup mode but with the comp UI. """
    CUP_LONG = "TrackMania/Legacy/TM_CupLong_Online.Script.txt"
    """ First player to win X maps wins the match. """
    CUP_SHORT = "TrackMania/Legacy/TM_CupShort_Online.Script.txt"
    """ First player to win the map wins the match. """
    TMWT_TEAMS = "TrackMania/TM_TMWC2023_Online.Script.txt"
    """ 2v2 teams, first team to 10 points wins the map, first to X maps wins the match. """

    # TODO support more script types


class PluginType(Enum):
    """
    The plugin type for a round. I'm actually not sure what other types there are.
    """

    EMPTY = ""
    CLUB = "server-plugins/Club/ClubPlugin.Script.txt"


class SpotType(Enum):
    """
    The stop type for a match. Determines how players are seeded in the match.
    """

    QUALIFICATION = "round_challenge_participant"
    SEED = "competition_participant"
    COMPETITION = "competition_leaderboard"
    TEAM = "competition_team"
    MATCH = "match_participant"


class AutoStartMode(Enum):
    """
    The auto start mode for a round. Determines the condition for when the round starts.
    """

    DELAY = "delay"
    """ Automatically start the match at start date + delay in seconds. """
    DISABLED = ""
    """ Disable auto start of match. """
    LIGHT = "light"
    """ The match starts automatically right away after the server starts. """


class RespawnBehavior(Enum):
    """
    The respawn behavior for a round. 
    """

    DEFAULT = 0
    """ Use the default behavior of the gamemode. """
    NORMAL = 1
    """ Use the normal behavior like in TimeAttack. """
    IGNORE = 2
    """ Do nothing. """
    GIVE_UP_FIRST_CP = 3
    """ Give up before the first checkpoint. """
    ALWAYS_GIVE_UP = 4
    """ Always give up. """
    NEVER_GIVE_UP = 5
    """ Never give up. """