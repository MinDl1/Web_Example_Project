import os
from dotenv import load_dotenv


load_dotenv()

TEST_USER = os.getenv("TEST_USER")
TEST_PASSWD = os.getenv("TEST_PASSWD")
