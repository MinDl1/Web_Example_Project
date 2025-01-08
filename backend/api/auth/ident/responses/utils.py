from fastapi import HTTPException

from ...errors import ErrorModel


def convert_to_example(http_exceptions: list[HTTPException]) -> dict:
    """Converts from list of HTTPException to dict response for swagger documentation.

    Args:
        http_exceptions: HTTP exceptions

    Returns:
        A dict of HTTP responses for swagger documentation.
    """
    examples = {}
    for http_exception in http_exceptions:
        examples[http_exception.status_code] = {
            "summary": http_exception.detail.get("code"),
            "value": {
                "detail": http_exception.detail
            }
        }

    return {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": examples
            }
        }
    }
