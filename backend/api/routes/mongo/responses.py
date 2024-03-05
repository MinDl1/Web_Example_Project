from fastapi import status

from .errors import ErrorModel, ErrorCode


mongo_post_responses = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.ID_EXISTS_ERROR: {
                        "summary": "ID_EXISTS_ERROR",
                        "value": {
                            "detail": {
                                "code": ErrorCode.ID_EXISTS_ERROR,
                                "reason": "ID exists"
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

mongo_get_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not found"
    }
}

mongo_get_one_patch_delete_responses = {
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
