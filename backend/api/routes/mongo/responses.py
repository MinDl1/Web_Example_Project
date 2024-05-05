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
    }
}

mongo_get_one_delete_responses = {
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
    }
}

mongo_patch_responses = {
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
                    ErrorCode.DATA_NOT_MODIFIED: {
                        "summary": "DATA_NOT_MODIFIED",
                        "value": {
                            "detail": {
                                "code": ErrorCode.DATA_NOT_MODIFIED,
                                "reason": "Book with ID, new data does not differ from the data in the database"
                            }
                        },
                    },
                }
            }
        },
    }
}
