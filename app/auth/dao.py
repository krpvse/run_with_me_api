from app.dao.base import BaseDAO
from app.profiles.models import Users, Runners


class UsersDAO(BaseDAO):
    model = Users


class RunnersDAO(BaseDAO):
    model = Runners
