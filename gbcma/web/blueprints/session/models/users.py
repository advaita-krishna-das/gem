from gbcma.event import Event


class SessionUsers:
    def __init__(self, session):
        self.__session = session
        self.__sockets = {}  # multiple sockets per one user is possible
        self.__changed = Event()

    @property
    def changed(self):
        return self.__changed

    @property
    def all(self):
        result = []
        ids_present = []
        users = self.__sockets.values()
        for user in users:
            user_id = user["id"]
            if user_id not in ids_present:
                result.append(user)
                ids_present.append(user_id)
        return result

    def is_socket_connected(self, socket_id):
        return socket_id in self.__sockets

    def join(self, socket_id, user):
        self.__sockets[socket_id] = self.__map(user)
        self.__notify_changes()
        self.__changed.notify(socket_id, user, True)

    def leave(self, socket_id):
        if socket_id not in self.__sockets:
            return

        user = self.__sockets[socket_id]
        del self.__sockets[socket_id]
        self.__notify_changes()
        self.__changed.notify(socket_id, user, False)

    def __notify_changes(self):
        self.__session.notify("users", self.all)

    @staticmethod
    def __map(user):
        return {"id": user.get_id(), "name": user.name}