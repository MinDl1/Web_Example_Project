import redis
from redis.exceptions import ConnectionError


class RedisTools:
    """
    Class for working with Redis
    """
    def __init__(self, url: str) -> None:
        self.__redis_connect = redis.from_url(url=url)
        self.__redis_connect.ping()

    def add_email_code(self, email: str, code: str) -> None:
        # Set email as key, code as value with TTL 15 minutes
        self.__redis_connect.setex(email, 900, code)

    def get_email_code(self, email: str) -> str | None:
        code = self.__redis_connect.get(email)

        if code:
            return code.decode('utf-8')

        return None

    def del_email_code(self, email: str) -> None:
        self.__redis_connect.delete(email)

    def __del__(self) -> None:
        self.__redis_connect.quit()
