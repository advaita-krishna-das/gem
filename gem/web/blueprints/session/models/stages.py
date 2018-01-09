from gem.db import sessions, proposals
from gem.event import Event

from ..stages import *


class SessionStages:
    def __init__(self, session):
        self.__session = session
        self.__stages = self.__create_stages(session.session_id)
        self.__stage_idx = 0

        self.__changed = Event()

    @property
    def changed(self):
        return self.__changed

    @property
    def index(self):
        return self.__stage_idx

    @property
    def count(self):
        return len(self.__stages)

    @property
    def current(self):
        return self.__stages[self.__stage_idx]

    @property
    def next(self):
        return self.__stages[self.__stage_idx + 1] if len(self.__stages) > self.__stage_idx + 1 else None

    def change(self, step=1):
        self.current.on_leave()
        self.__stage_idx += step
        if self.__stage_idx <= 0:
            self.__stage_idx = 0
        if self.__stage_idx >= len(self.__stages):
            self.__stage_idx = len(self.__stages) - 1

        self.current.on_enter()
        self.__changed.notify(self.current)

        return {
            "current": {
                "title": self.current.proposal["title"] if self.current.proposal else ""
            },
            "next": {
                "title": self.next.proposal["title"] if self.next and self.next.proposal else "",
                "type": self.next.name if self.next else ""
            }
        }

    def __create_stages(self, session_id):
        result = []
        session = sessions.get(session_id)  # gets session document
        docs = proposals.get_list(session["proposals"])

        for idx, proposal in enumerate(docs):
            stages = [
                AcquaintanceSessionStage(self.__session, proposal),
                DiscussionSessionStage(self.__session, proposal),
                CommentingSessionStage(self.__session, proposal),
                VotingSessionStage(self.__session, proposal),
                VotingResultsSessionStage(self.__session, proposal)]

            for stage in stages:
                stage.changed.subscribe(self.__on_stage_changed)
                result.append(stage)

        result.append(ClosedSessionStage(self.__session))
        result.insert(0, AgendaSessionStage(self.__session, result))
        return result

    def __on_stage_changed(self, *options):
        self.__changed.notify(self.current)
