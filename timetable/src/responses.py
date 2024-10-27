from src.exceptions import ErrorResponseModel

timetable_400 = {
    "description": "Timetable is already passed.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Timetable is already passed."
            }
        }
    }
}

appointments_booking_400 = {
    "description": "Timetable is not available for this time.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Timetable is not available for this time."
            }
        }
    }
}

appointments_delete_400 = {
    "description": "Appointment already booked.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Cannot delete a meeting that has started."
            }
        }
    }
}

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

appointments_403 = {
    "description": "You are not authorized to perform this action.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "You are not authorized to delete this appointment."
            }
        }
    }
}

full_403 = {
    "description": "Not enough privileges.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Not enough privileges."
            }
        }
    }
}

create_404 = {
    "description": "Resource not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "examples": {
                "doctor_not_found": {"summary": "Doctor Not Found", "value": {"detail": "Doctor not found."}},
                "hospital_not_found": {"summary": "Hospital Not Found", "value": {"detail": "Hospital not found."}},
                "room_not_found": {"summary": "Room Not Found", "value": {"detail": "Room not found."}},
            }
        }
    }
}

timetable_404 = {
    "description": "Timetable not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Timetable not found."
            }
        }
    }
}

appointments_404 = {
    "description": "Appointments not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Appointment not found."
            }
        }
    }
}

hospital_404 = {
    "description": "Hospital not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Hospital not found."
            }
        }
    }
}

doctor_404 = {
    "description": "Doctor not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Doctor not found."
            }
        }
    }
}

room_404 = {
    "description": "Resource not found.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "examples": {
                "hospital_not_found": {"summary": "Hospital Not Found", "value": {"detail": "Hospital not found."}},
                "room_not_found": {"summary": "Room Not Found", "value": {"detail": "Room not found."}},
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
                "timetable_not_found": {"summary": "Timetable Not Found", "value": {"detail": "Timetable not found."}},
                "doctor_not_found": {"summary": "Doctor Not Found", "value": {"detail": "Doctor not found."}},
                "hospital_not_found": {"summary": "Hospital Not Found", "value": {"detail": "Hospital not found."}},
                "room_not_found": {"summary": "Room Not Found", "value": {"detail": "Room not found."}},
            }
        }
    }
}

timetable_409 = {
    "description": "Timetable already has appointments.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Timetable already has appointments."
            }
        }
    }
}

appointments_409 = {
    "description": "Appointment already booked.",
    "model": ErrorResponseModel,
    "content": {
        "application/json": {
            "example": {
                "detail": "Appointment already booked."
            }
        }
    }
}








