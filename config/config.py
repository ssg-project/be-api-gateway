import os
from dotenv import load_dotenv

if not os.getenv("APP_ENV"):
    load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

TICKETING_USER_URL = os.getenv("TICKETING_USER_URL")
TICKETING_TICKETING_URL = os.getenv("TICKETING_TICKETING_URL")
TICKETING_EVENT_URL = os.getenv("TICKETING_EVENT_URL")
GATEWAY_URL = os.getenv("GATEWAY_URL")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")