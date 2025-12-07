from typing import Optional, Dict


class AppException(Exception):
    """
    Base application exception for custom error handling.
    """

    def __init__(
        self, message: str, status_code: int = 500, detail: Optional[Dict] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.detail = detail


class EntityNotFoundException(AppException):
    """
    Exception for entity not found errors (HTTP 404).
    """

    def __init__(self, message: str, detail: Optional[Dict] = None):
        super().__init__(message, status_code=404, detail=detail)

    @staticmethod
    def not_found(entity_name: str, entity_id: int) -> "EntityNotFoundException":
        message = f"{entity_name} with id {entity_id} not found."
        detail = {"entity": entity_name, "id": entity_id}
        return EntityNotFoundException(message, detail)


class ValidationException(AppException):
    """
    Exception for validation errors (HTTP 400).
    """

    def __init__(self, message: str, detail: Optional[Dict] = None):
        super().__init__(message, status_code=400, detail=detail)

    @staticmethod
    def invalid_data(field: str, reason: str) -> "ValidationException":
        message = f"Invalid data for field '{field}': {reason}."
        detail = {"field": field, "reason": reason}
        return ValidationException(message, detail)


class DuplicateEntityException(AppException):
    """
    Exception for duplicate entity errors (HTTP 409).
    """

    def __init__(self, message: str, detail: Optional[Dict] = None):
        super().__init__(message, status_code=409, detail=detail)

    @staticmethod
    def duplicate(
        entity_name: str, field: str, value: str
    ) -> "DuplicateEntityException":
        message = f"Duplicate {entity_name}: {field} '{value}' already exists."
        detail = {"entity": entity_name, "field": field, "value": value}
        return DuplicateEntityException(message, detail)
