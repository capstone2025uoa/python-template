import json
import logging
import aioboto3
from typing import Dict, Any, Optional, Union

# Get a logger for this module - configuration should be done in app.py
logger = logging.getLogger(__name__)

class SQSClient:
    """Asynchronous client for interacting with AWS SQS queues."""
    
    def __init__(self, queue_url: str, region_name: str = "ap-southeast-2", endpoint_url: Optional[str] = None):
        """
        Initialize the SQS client.
        
        Args:
            queue_url: The URL of the SQS queue to send messages to
            region_name: AWS region to connect to
            endpoint_url: Optional endpoint URL for local development with LocalStack
        """
        self.region_name = region_name
        self.queue_url = queue_url
        self.endpoint_url = endpoint_url
        self.session = aioboto3.Session()
    
    async def __aenter__(self):
        """Support for async with statement."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the async context."""
        pass  # The aioboto3 client handles closing resources
    
    async def send_message(self, 
                       message_body: Union[str, Dict[str, Any]], 
                       message_type: str = "template", 
                       content_type: str = "application/json", 
                       queue_url: str = None, 
                       delay_seconds: int = 0) -> Dict[str, Any]:
        """
        Send a message to an SQS queue.
        
        Args:
            message_body: The message to send (string or dictionary)
            message_type: Value for the Message-Type attribute
            content_type: Value for the Content-Type attribute
            queue_url: Optional override for the queue URL (defaults to the one provided at initialization)
            delay_seconds: The time in seconds to delay the message
            
        Returns:
            SQS response containing MessageId and other metadata
        """
        # Use default queue URL if not provided
        queue_url = queue_url or self.queue_url
        
        # Convert dict to JSON string if needed
        if isinstance(message_body, dict):
            message_body = json.dumps(message_body)
        
        # Standard message attributes
        message_attributes = {
            'Message-Type': {
                'DataType': 'String',
                'StringValue': message_type
            },
            'Content-Type': {
                'DataType': 'String',
                'StringValue': content_type
            }
        }
        
        async with self.session.client('sqs', region_name=self.region_name, 
                                     endpoint_url=self.endpoint_url) as sqs:
            try:
                response = await sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=message_body,
                    DelaySeconds=delay_seconds,
                    MessageAttributes=message_attributes
                )
                
                logger.info(f"Message sent to queue {queue_url}, MessageId: {response.get('MessageId')}")
                return response
            except Exception as e:
                logger.error(f"Error sending message to SQS queue {queue_url}: {str(e)}")
                raise
    
    async def send_text_message(self, 
                           text: str,
                           message_type: str = "template",
                           queue_url: str = None,
                           delay_seconds: int = 0) -> Dict[str, Any]:
        """
        Send a plain text message to an SQS queue.
        
        Args:
            text: The text message to send
            message_type: Value for the Message-Type attribute (defaults to "template")
            queue_url: Optional override for the queue URL
            delay_seconds: The time in seconds to delay the message
            
        Returns:
            SQS response containing MessageId and other metadata
        """
        return await self.send_message(
            message_body=text,
            message_type=message_type,
            content_type="text/plain",
            queue_url=queue_url,
            delay_seconds=delay_seconds
        )
    
    async def send_json_message(self, 
                           data: Dict[str, Any],
                           message_type: str = "template",
                           queue_url: str = None,
                           delay_seconds: int = 0) -> Dict[str, Any]:
        """
        Send a JSON message to an SQS queue.
        
        Args:
            data: The dictionary to send as JSON
            message_type: Value for the Message-Type attribute (defaults to "template") 
            queue_url: Optional override for the queue URL
            delay_seconds: The time in seconds to delay the message
            
        Returns:
            SQS response containing MessageId and other metadata
        """
        return await self.send_message(
            message_body=data,
            message_type=message_type,
            content_type="application/json",
            queue_url=queue_url,
            delay_seconds=delay_seconds
        )


async def example_usage():
    """Example of how to use the SQSClient."""
    # Define the SQS queue URL and region for AWS
    queue_url = "https://sqs.ap-southeast-2.amazonaws.com/343218181976/template-sqs"
    region = "ap-southeast-2"
    
    # Create a client with explicit configuration
    async with SQSClient(queue_url=queue_url, region_name=region) as sqs_client:
        # Example 1: Send a JSON message
        json_response = await sqs_client.send_json_message(
            data={"abc": "abc"}
        )
        
        # Example 2: Send a plain text message
        text_response = await sqs_client.send_text_message(
            text="Hello, this is a plain text message"
        )
        
        # Example 3: Using the general send_message method
        default_response = await sqs_client.send_message(
            message_body={"data": "Using general method"}
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())