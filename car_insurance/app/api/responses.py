ERROR_RESPONSES = {
    400: {"description": "Bad Request"},
    422: {"description": "Unprocessable Entity"},
    404: {"description": "Resource not found"},
    409: {"description": "Conflict"},
    500: {"description": "Internal Server Error"},
}


def error_responses(*codes: int) -> dict:
    return {code: ERROR_RESPONSES[code] for code in codes}
