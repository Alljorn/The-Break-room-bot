
class UserAlreadyExist(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"'{user_id}' user id already exists in table")

class UserNotExist(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"'{user_id}' user id does not exist in table")

class RoleNotReferenced(Exception):
    def __init__(self, role_name: str) -> None:
        super().__init__(f"'{role_name}' user role do not referenced by the User Manager")


class UserAlreadyConnected(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"'{user_id}' user is already connected")

class UserNotConnected(Exception):
    def __init__(self) -> None:
        super().__init__("User is not connected")

class UserNoEnoughPermission(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"'{user_id}' user does not have enough permission")


class UserInventoryAlreadyExist(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"'{user_id}' user inventory id already exists in table")


class SupplyAlreadyExist(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"'{name}' supply name already exists in table")

class SupplyNotExist(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"'{name}' supply name does not exist in table")

class TypeNotReferenced(Exception):
    def __init__(self, type_name: str) -> None:
        super().__init__(f"'{type_name}' type do not referenced by the Supply Manager")

class EffectNotExist(Exception):
    def __init__(self, effect_name: str) -> None:
        super().__init__(f"'{effect_name}' effect name does not exist in table")


class SupplyNotInInventory(Exception):
    def __init__(self, user_id: int, supply_name: str) -> None:
        super().__init__(f"'{supply_name} supply name is not in inventory of {user_id} user id")
