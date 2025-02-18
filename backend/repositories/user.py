from backend.models import User
from backend.repositories import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User
