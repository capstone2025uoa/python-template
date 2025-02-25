import asyncio
import logging
from adapters.sqs.router import route_message
from adapters.sqs.sqs_session import get_sqs_client
from config import SQS_QUEUE_URL

logger = logging.getLogger(__name__)

async def receive_message(queue_url: str):
    async with await get_sqs_client() as client:
        response = await client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,
            VisibilityTimeout=20,
            MessageAttributeNames=["All"]
        )
    return response.get("Messages", [])

async def poll_messages(queue_url: str = SQS_QUEUE_URL, delete_unknown_types: bool = True):
    messages = await receive_message(queue_url)
    if not messages:
        return

    # Process each message and track which ones should be deleted
    results = await asyncio.gather(
        *(route_message(message, delete_unknown_types) for message in messages),
        return_exceptions=True
    )
    
    # Determine which messages to delete
    messages_to_delete = []
    for i, result in enumerate(results):
        message = messages[i]
        
        # Handle exceptions raised during processing
        if isinstance(result, Exception):
            logger.error(f"Error routing message {message.get('MessageId')}: {str(result)}")
            continue
            
        # If result is True, the message was successfully processed or should be deleted
        if result:
            messages_to_delete.append({
                "Id": message["MessageId"],
                "ReceiptHandle": message["ReceiptHandle"]
            })
    
    # Delete messages that were successfully processed or should be deleted
    if messages_to_delete:
        async with await get_sqs_client() as client:
            try:
                response = await client.delete_message_batch(
                    QueueUrl=queue_url,
                    Entries=messages_to_delete
                )
                
                # Log any failed deletions
                if "Failed" in response and response["Failed"]:
                    for failed in response["Failed"]:
                        logger.error(f"Failed to delete message: {failed}")
                        
                logger.info(f"Deleted {len(response.get('Successful', []))} messages from queue")
            except Exception as e:
                logger.error(f"Error deleting messages: {str(e)}")

async def poll_loop(interval: float = 0.1, delete_unknown_types: bool = True):
    logger.info("Starting SQS poll loop")
    while True:
        try:
            await poll_messages(SQS_QUEUE_URL, delete_unknown_types)
        except Exception as error:
            logger.error(f"Error polling messages: {error}")
        await asyncio.sleep(interval)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(poll_loop())