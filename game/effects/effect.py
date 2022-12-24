
class Effect:
    
    def __init__(self, name='none') -> None:
        self.__name = name

    def __repr__(self) -> str:
        return self.__name