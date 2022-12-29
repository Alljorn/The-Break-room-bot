
class UserAlreadyExist(Exception):
    def __init__(self, id: int) -> None:
        message = f"'{id}' user id already exists in table"
        super().__init__(message)

class UserDoNotExist(Exception):
    def __init__(self, id: int) -> None:
        message = f"'{id}' user id does not exist in table"
        super().__init__(message)

class UserRoleDoNotReferenced(Exception):
    def __init__(self, role: str) -> None:
        message = f"'{role}' user role do not referenced by the User Manager"
        super().__init__(message)