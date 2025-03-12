import os
from dotenv import load_dotenv
import boto3
import json
from botocore.exceptions import ClientError

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

else:
    secret_name = "secret/ticketing/gateway"
    region_name = "ap-northeast-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    
    secret_data = json.loads(secret)

    JWT_SECRET_KEY = secret_data["JWT_SECRET_KEY"]
    JWT_ALGORITHM = secret_data["JWT_ALGORITHM"]

    TICKETING_USER_URL = secret_data["TICKETING_USER_URL"]
    TICKETING_TICKETING_URL = secret_data["TICKETING_TICKETING_URL"]
    TICKETING_EVENT_URL = secret_data["TICKETING_EVENT_URL"]
    GATEWAY_URL = secret_data["GATEWAY_URL"]

    REDIS_HOST = secret_data["REDIS_HOST"]
    REDIS_PORT = secret_data["REDIS_PORT"]
