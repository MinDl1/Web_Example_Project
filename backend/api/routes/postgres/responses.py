from fastapi import status

from .errors import ErrorModel, ErrorCode


postgres_post_responses = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.UNIQUE_ERROR: {
                        "summary": "UNIQUE_ERROR",
                        "value": {
                            "detail": {
                                "code": ErrorCode.UNIQUE_ERROR,
                                "reason": "Unique value"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not found"
    }
}

postgres_get_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not found"
    }
}

postgres_get_one_delete_responses = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.ID_NOT_FOUND: {
                        "summary": "ID_NOT_FOUND",
                        "value": {
                            "detail": {
                                "code": ErrorCode.ID_NOT_FOUND,
                                "reason": "ID not found"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not found"
    }
}

postgres_patch_responses = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.ID_NOT_FOUND: {
                        "summary": "ID_NOT_FOUND",
                        "value": {
                            "detail": {
                                "code": ErrorCode.ID_NOT_FOUND,
                                "reason": "ID not found"
                            }
                        },
                    },
                    ErrorCode.UNIQUE_ERROR: {
                        "summary": "UNIQUE_ERROR",
                        "value": {
                            "detail": {
                                "code": ErrorCode.UNIQUE_ERROR,
                                "reason": "Unique value"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not found"
    }
}
