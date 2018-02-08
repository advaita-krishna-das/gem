from gem.db.core.repository import Repository
from gem.db.config import za


class ZaRepository(Repository):
    """Provides interface for Za collection of database."""

    def __init__(self):
        super().__init__(za)

#    def with_permission(self, permission):
#        # todo not effective
#        from gem.db import roles

#        result = []
#        for user in self.all():
#            role = roles.find_one({"name": user.role})
#            if permission in role.permissions:
#                result.append(user)
#        return result
