from fastapi import status

from routes.auth.errors import ErrorCode, ErrorModel


all_endpoints_get_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "Could not validate credentials"
                            }
                        },
                    },
                    ErrorCode.INVALID_TOKEN: {
                        "summary": "INVALID_TOKEN",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVALID_TOKEN,
                                "reason": "INVALID_TOKEN"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "Access token expires but refresh exists"
                            }
                        },
                    },
                    ErrorCode.NO_ACCESS_RIGHTS: {
                        "summary": "NO_ACCESS_RIGHTS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.NO_ACCESS_RIGHTS,
                                "reason": "No required access rights"
                            }
                        },
                    },
                    ErrorCode.LOGIN_USER_IS_NOT_ACTIVE: {
                        "summary": "LOGIN_USER_IS_NOT_ACTIVE",
                        "value": {
                            "detail": {
                                "code": ErrorCode.LOGIN_USER_IS_NOT_ACTIVE,
                                "reason": "LOGIN_USER_IS_NOT_ACTIVE"
                            }
                        },
                    },
                }
            }
        },
    }
}