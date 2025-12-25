from fastapi import HTTPException, status


class SQLError(Exception):
    pass

class HTTPError(HTTPException):
    exist = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Already exists")

    not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found")

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password")

    unavailable = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Function is unavailable")

    db_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Database error"
    )