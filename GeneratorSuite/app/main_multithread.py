class AppError(Exception):
    """Базовый класс для всех исключений приложения."""
    pass

class InvalidInputError(AppError):
    """Исключение для некорректного ввода данных."""
    pass

class PetNotFoundError(AppError):
    """Исключение, если питомец не найден в базе данных."""
    pass

class DatabaseError(AppError):
    """Исключение для ошибок, связанных с базой данных."""
    pass