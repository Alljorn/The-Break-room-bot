
class UserAlreadyExist(Exception):
    def __init__(self, id: int) -> None:
        message = f"'{id}' user id already exists in table"
        super().__init__(message)

class UserNotExist(Exception):
    def __init__(self, id: int) -> None:
        message = f"'{id}' user id does not exist in table"
        super().__init__(message)

class RoleNotReferenced(Exception):
    def __init__(self, role: str) -> None:
        message = f"'{role}' user role do not referenced by the User Manager"
        super().__init__(message)


class UserAlreadyConnected(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"'{id}' user is already connected")

class UserNotConnected(Exception):
    def __init__(self) -> None:
        super().__init__("User is not connected")