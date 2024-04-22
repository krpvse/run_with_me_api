from app.services.base import BaseService
from app.profiles.models import Users, Runners


class UsersService(BaseService):
    model = Users


class RunnersService(BaseService):
    model = Runners
