class EmptyFieldException(Exception):
    pass

class IdNotFoundException(Exception):
    def __init__(self, message="Данные не найдены"):
        super().__init__(message)

class IdAlreadyInventoriedException(Exception):
    pass