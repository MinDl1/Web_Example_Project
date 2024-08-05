from fastapi import status

from routes.auth.errors import ErrorCode, ErrorModel


user_me_get_responses = {
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
                                "reason": "User with id ... not found"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.INVALID_TOKEN: {
                        "summary": "INVALID_TOKEN",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVALID_TOKEN,
                                "reason": "INVALID_TOKEN"
                            }
                        },
                    },
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "Could not validate credentials"
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
                }
            }
        },
    }
}

user_me_patch_responses = {
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
                                "reason": "User with id ... not found"
                            }
                        },
                    },
                    ErrorCode.VALUE_ERROR: {
                        "summary": "VALUE_ERROR",
                        "value": {
                            "detail": {
                                "code": ErrorCode.VALUE_ERROR,
                                "reason": "No fields to update"
                            }
                        },
                    },
                    ErrorCode.UNIQUE_ERROR: {
                        "summary": "UNIQUE_ERROR",
                        "value": {
                            "detail": {
                                "code": ErrorCode.UNIQUE_ERROR,
                                "reason": "Unique value error"
                            }
                        },
                    },
                    ErrorCode.BAD_EMAIL: {
                        "summary": "BAD_EMAIL",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_EMAIL,
                                "reason": "Not an email entered"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.INVALID_TOKEN: {
                        "summary": "INVALID_TOKEN",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVALID_TOKEN,
                                "reason": "INVALID_TOKEN"
                            }
                        },
                    },
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "Could not validate credentials"
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

user_me_delete_responses = {
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
                                "reason": "User with id ... not found"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.INVALID_TOKEN: {
                        "summary": "INVALID_TOKEN",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVALID_TOKEN,
                                "reason": "INVALID_TOKEN"
                            }
                        },
                    },
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "Could not validate credentials"
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

all_user_get_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.INVALID_TOKEN: {
                        "summary": "INVALID_TOKEN",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVALID_TOKEN,
                                "reason": "INVALID_TOKEN"
                            }
                        },
                    },
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "Could not validate credentials"
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
                    ErrorCode.LOGIN_USER_IS_NOT_ACTIVE: {
                        "summary": "LOGIN_USER_IS_NOT_ACTIVE",
                        "value": {
                            "detail": {
                                "code": ErrorCode.LOGIN_USER_IS_NOT_ACTIVE,
                                "reason": "LOGIN_USER_IS_NOT_ACTIVE"
                            }
                        },
                    },
                    ErrorCode.NOT_ADMIN_USER: {
                        "summary": "NOT_ADMIN_USER",
                        "value": {
                            "detail": {
                                "code": ErrorCode.NOT_ADMIN_USER,
                                "reason": "NOT_ADMIN_USER"
                            }
                        },
                    },
                }
            }
        },
    }
}

user_get_responses = {
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
                                "reason": "User with id id_u not found"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.INVALID_TOKEN: {
                        "summary": "INVALID_TOKEN",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVALID_TOKEN,
                                "reason": "INVALID_TOKEN"
                            }
                        },
                    },
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "Could not validate credentials"
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
                    ErrorCode.LOGIN_USER_IS_NOT_ACTIVE: {
                        "summary": "LOGIN_USER_IS_NOT_ACTIVE",
                        "value": {
                            "detail": {
                                "code": ErrorCode.LOGIN_USER_IS_NOT_ACTIVE,
                                "reason": "LOGIN_USER_IS_NOT_ACTIVE"
                            }
                        },
                    },
                    ErrorCode.NOT_ADMIN_USER: {
                        "summary": "NOT_ADMIN_USER",
                        "value": {
                            "detail": {
                                "code": ErrorCode.NOT_ADMIN_USER,
                                "reason": "NOT_ADMIN_USER"
                            }
                        },
                    },
                }
            }
        },
    }
}

user_patch_responses = {
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
                                "reason": "User with id id_u not found"
                            }
                        },
                    },
                    ErrorCode.VALUE_ERROR: {
                        "summary": "VALUE_ERROR",
                        "value": {
                            "detail": {
                                "code": ErrorCode.VALUE_ERROR,
                                "reason": "No fields to update"
                            }
                        },
                    },
                    ErrorCode.UNIQUE_ERROR: {
                        "summary": "UNIQUE_ERROR",
                        "value": {
                            "detail": {
                                "code": ErrorCode.UNIQUE_ERROR,
                                "reason": "Unique value error"
                            }
                        },
                    },
                    ErrorCode.BAD_EMAIL: {
                        "summary": "BAD_EMAIL",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_EMAIL,
                                "reason": "Not an email entered"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.INVALID_TOKEN: {
                        "summary": "INVALID_TOKEN",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVALID_TOKEN,
                                "reason": "INVALID_TOKEN"
                            }
                        },
                    },
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "Could not validate credentials"
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
                    ErrorCode.LOGIN_USER_IS_NOT_ACTIVE: {
                        "summary": "LOGIN_USER_IS_NOT_ACTIVE",
                        "value": {
                            "detail": {
                                "code": ErrorCode.LOGIN_USER_IS_NOT_ACTIVE,
                                "reason": "LOGIN_USER_IS_NOT_ACTIVE"
                            }
                        },
                    },
                    ErrorCode.NOT_ADMIN_USER: {
                        "summary": "NOT_ADMIN_USER",
                        "value": {
                            "detail": {
                                "code": ErrorCode.NOT_ADMIN_USER,
                                "reason": "NOT_ADMIN_USER"
                            }
                        },
                    },
                }
            }
        },
    }
}

user_delete_responses = {
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
                                "reason": "User with id id_u not found"
                            }
                        },
                    },
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.INVALID_TOKEN: {
                        "summary": "INVALID_TOKEN",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVALID_TOKEN,
                                "reason": "INVALID_TOKEN"
                            }
                        },
                    },
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "Could not validate credentials"
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
                    ErrorCode.LOGIN_USER_IS_NOT_ACTIVE: {
                        "summary": "LOGIN_USER_IS_NOT_ACTIVE",
                        "value": {
                            "detail": {
                                "code": ErrorCode.LOGIN_USER_IS_NOT_ACTIVE,
                                "reason": "LOGIN_USER_IS_NOT_ACTIVE"
                            }
                        },
                    },
                    ErrorCode.NOT_ADMIN_USER: {
                        "summary": "NOT_ADMIN_USER",
                        "value": {
                            "detail": {
                                "code": ErrorCode.NOT_ADMIN_USER,
                                "reason": "NOT_ADMIN_USER"
                            }
                        },
                    },
                }
            }
        },
    }
}
