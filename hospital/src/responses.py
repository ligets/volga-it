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

hospital_404 = {
    'description': 'Hospital not found.',
    'model': ErrorResponseModel,
    'content': {
        'application/json': {
            'example': {
                "detail": "Hospital not found."
            }
        }
    }
}

full_404 = {
    'description': 'Not Found.',
    'model': ErrorResponseModel,
    'content': {
        'application/json': {
            'examples': {
                "hospital_not_fount": {"summary": "Hospital not found.", "value": {"detail": "Hospital not found."}},
                "room_not_found": {"summary": "Room not found.", "value": {"detail": "Room not found."}}
            }
        }
    }
}

