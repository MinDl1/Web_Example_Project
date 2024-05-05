from fastapi import status

from routes.auth.errors import ErrorCode, ErrorModel


create_role_post_responses = {
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
                    ErrorCode.ID_NOT_FOUND: {
                        "summary": "ID_NOT_FOUND",
                        "value": {
                            "detail": {
                                "code": ErrorCode.ID_NOT_FOUND,
                                "reason": "Role with name ... not found"
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

all_role_get_responses = {
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

role_get_responses = {
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
                                "reason": "Role with id id_r not found"
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

role_patch_responses = {
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
                                "reason": "Role with id id_r not found"
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

role_delete_responses = {
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
                                "reason": "Role with id id_r not found"
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
