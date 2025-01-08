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
                    ErrorCode.BAD_CREDENTIALS: {
                        "summary": "BAD_CREDENTIALS",
                        "value": {
                            "detail": {
                                "code": ErrorCode.BAD_CREDENTIALS,
                                "reason": "BAD_CREDENTIALS"
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
                }
            }
        },
    },
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

create_user_post_responses = {
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
                                "reason": "Unique value error"
                            }
                        },
                    },
                    ErrorCode.FOREIGN_KEY_ERROR: {
                        "summary": "FOREIGN_KEY_ERROR",
                        "value": {
                            "detail": {
                                "code": ErrorCode.FOREIGN_KEY_ERROR,
                                "reason": "Foreign key error in ..."
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

all_user_get_responses = {
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

user_patch_responses = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.INVULNERABLE_USER: {
                        "summary": "INVULNERABLE_USER",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVULNERABLE_USER,
                                "reason": "User with id ... is invulnerable"
                            }
                        },
                    },
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
                    ErrorCode.FOREIGN_KEY_ERROR: {
                        "summary": "FOREIGN_KEY_ERROR",
                        "value": {
                            "detail": {
                                "code": ErrorCode.FOREIGN_KEY_ERROR,
                                "reason": "Foreign key error in ..."
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

user_delete_responses = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.INVULNERABLE_USER: {
                        "summary": "INVULNERABLE_USER",
                        "value": {
                            "detail": {
                                "code": ErrorCode.INVULNERABLE_USER,
                                "reason": "User with id ... is invulnerable"
                            }
                        },
                    },
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
