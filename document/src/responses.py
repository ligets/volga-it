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

view_403 = {
    "description": "Forbidden request.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "You are not authorized to view this history."
            }
        }
    }
}

forb_403 = {
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

full_404 = {
    "description": "Resource not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "examples": {
                "history_not_found:": {"summary": "History Not Found", "value": {"detail": "History not found."}},
                "pacient_not_found:": {"summary": "Pacient Not Found", "value": {"detail": "Pacient not found."}},
                "doctor_not_found:": {"summary": "Doctor Not Found", "value": {"detail": "Doctor not found."}},
                "hospital_not_found:": {"summary": "Hospital Not Found", "value": {"detail": "Hospital not found."}},
                "room_not_found:": {"summary": "Room Not Found", "value": {"detail": "Room not found."}},
            }
        }
    }
}

validate_404 = {
    "description": "Resource not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "examples": {
                "pacient_not_found:": {"summary": "Pacient Not Found", "value": {"detail": "Pacient not found."}},
                "doctor_not_found:": {"summary": "Doctor Not Found", "value": {"detail": "Doctor not found."}},
                "hospital_not_found:": {"summary": "Hospital Not Found", "value": {"detail": "Hospital not found."}},
                "room_not_found:": {"summary": "Room Not Found", "value": {"detail": "Room not found."}},
            }
        }
    }
}

pacient_404 = {
    "description": "Resource not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Pacient not found.",
            }
        }
    }
}

history_404 = {
    "description": "Resource not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "History not found.",
            }
        }
    }
}
