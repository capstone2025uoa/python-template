import aioboto3
from config import SQS_QUEUE_URL, SQS_REGION

if not SQS_QUEUE_URL or not SQS_REGION:
    raise Exception("SQS_QUEUE_URL and SQS_REGION must be set")

session = aioboto3.Session()

async def get_sqs_client():
    return session.client("sqs", region_name=SQS_REGION)
