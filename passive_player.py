from config import *


def get_class_name():
    return 'PassivePlayer'


class PassivePlayer:
    """Passive Kingsheep player (doesn't move)"""

    def __init__(self):
        self.name = "PassivePlayer"
        self.uzh_shortname = "pplayer"

    def move_sheep(self, p_num, p_state, p_time_remaining, field):
        return MOVE_NONE, p_state

    def move_wolf(self, p_num, p_state, p_time_remaining, field):
        return MOVE_NONE, p_state
