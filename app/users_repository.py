from attrs import define
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: str
    full_name: str
    password: str
    id: int = 0


class UsersRepository:

    def __init__(self):
        self.users: list[User] = []

    # необходимые методы сюда
    def save(self, new_user: User):
        new_user.id = len(self.users) + 1
        self.users.append(new_user)

    def get_all(self):
        return self.users
    
    def get_by_email(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    def get_by_id(self, id: int) -> User:
        for user in self.users:
            if user.id == id:
                return user
        return None



    # конец решения
