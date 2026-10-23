class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"
    def __init__(self, *args, **kargs):
        super().__init__(self.detail, *args, **kargs)

class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"

