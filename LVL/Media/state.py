from enum import Enum


class State(Enum):
    WATCHED = 'WATCHED'
    IN_PROGRESS = 'IN_PROGRESS'
    UNWATCHED = 'UNWATCHED'


    @staticmethod
    def make_human_readable(state):
        human_readable = {
            State.WATCHED: 'Watched',
            State.IN_PROGRESS: 'In Progress',
            State.UNWATCHED: 'Unwatched'
        }
        return human_readable.get(state, state)