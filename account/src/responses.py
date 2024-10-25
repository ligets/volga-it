from src.exceptions import ErrorResponseModel

full_401 = {
    "description": "Not authenticated or Invalid token or Token has expired.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "examples": {
                "not_authenticated": {"summary": "Not Authenticated", "value": {"detail": "Not authenticated"}},
                "invalid_token": {"summary": "Invalid Token", "value": {"detail": "Invalid token."}},
                "token_expired": {"summary": "Token Expired", "value": {"detail": "Token has expired."}},
            }
        }
    }
}

tokens_401 = {
    "description": "Invalid token or Token has expired.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "examples": {
                "invalid_token": {"summary": "Invalid Token", "value": {"detail": "Invalid token."}},
                "token_expired": {"summary": "Token Expired", "value": {"detail": "Token has expired."}},
            }
        }
    }
}

full_403 = {
    "description": "Forbidden request.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Not enough privileges."
            }
        }
    }
}

username_409 = {
    'description': 'Conflict unique attribute',
    'model': ErrorResponseModel,
    'content': {
        'application/json': {
             'example': {
                 'detail': 'Username is already taken.'
             }
        }
    }
}
user_404 = {
    'description': 'User not found',
    'model': ErrorResponseModel,
    'content': {
        'application/json': {
             'example': {
                 'detail': 'User not found.'
             }
        }
    }
}
doctor_404 = {
    'description': 'Doctor not found',
    'model': ErrorResponseModel,
    'content': {
        'application/json': {
             'example': {
                 'detail': 'Doctor not found.'
             }
        }
    }
}
