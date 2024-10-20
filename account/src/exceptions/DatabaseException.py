from fastapi import HTTPException, status


class DatabaseException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Exc: Cannot insert data into table"
        )


class UnknownDatabaseException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unknown Exc: Cannot insert data into table"
        )


class ConflictUniqueAttribute(HTTPException):
    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
