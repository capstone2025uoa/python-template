import json
import logging
import aioboto3
from typing import Dict, Any, Optional, Union

# Get a logger for this module - configuration should be done in app.py
logger = logging.getLogger(__name__)

class SNSClient:
    """Asynchronous client for interacting with AWS SNS topics."""
    
    def __init__(self, topic_arn: str, region_name: str = None, endpoint_url: Optional[str] = None):
        """
        Initialize the SNS client.
        
        Args:
            topic_arn: The ARN of the SNS topic to publish to
            region_name: AWS region to connect to (extracted from ARN if not provided)
            endpoint_url: Optional endpoint URL for local development
        """
        self.topic_arn = topic_arn
        
        # Extract region from the topic ARN if not explicitly provided
        if region_name is None and topic_arn:
            # Format: arn:aws:sns:region:account:topic
            parts = topic_arn.split(':')
            if len(parts) >= 4:
                region_name = parts[3]
        
        self.region_name = region_name
        self.endpoint_url = endpoint_url
        self.session = aioboto3.Session()
    
    async def __aenter__(self):
        """Support for async with statement."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the async context."""
        pass  # The aioboto3 client handles closing resources
    
    async def publish_message(self, 
                          message: Union[str, Dict[str, Any]], 
                          message_type: str = "template", 
                          content_type: str = "application/json", 
                          topic_arn: str = None,
                          subject: str = None) -> Dict[str, Any]:
        """
        Publish a message to an SNS topic.
        
        Args:
            message: The message to publish (string or dictionary)
            message_type: Value for the Message-Type attribute
            content_type: Value for the Content-Type attribute
            topic_arn: Optional override for the topic ARN (defaults to the one provided at initialization)
            subject: Optional subject for the message (useful for email subscriptions)
            
        Returns:
            SNS response containing MessageId and other metadata
        """
        # Use default topic ARN if not provided
        topic_arn = topic_arn or self.topic_arn
        
        # Convert dict to JSON string if needed
        if isinstance(message, dict):
            message = json.dumps(message)
        
        # Standard message attributes - keeping consistent with SQS client
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
        
        async with self.session.client('sns', region_name=self.region_name, 
                                     endpoint_url=self.endpoint_url) as sns:
            try:
                publish_params = {
                    'TopicArn': topic_arn,
                    'Message': message,
                    'MessageAttributes': message_attributes
                }
                
                if subject:
                    publish_params['Subject'] = subject
                
                response = await sns.publish(**publish_params)
                
                logger.info(f"Message published to topic {topic_arn}, MessageId: {response.get('MessageId')}")
                return response
            except Exception as e:
                logger.error(f"Error publishing message to SNS topic {topic_arn}: {str(e)}")
                raise
    
    async def publish_text_message(self, 
                              text: str,
                              message_type: str = "template",
                              topic_arn: str = None,
                              subject: str = None) -> Dict[str, Any]:
        """
        Publish a plain text message to an SNS topic.
        
        Args:
            text: The text message to publish
            message_type: Value for the Message-Type attribute (defaults to "template")
            topic_arn: Optional override for the topic ARN
            subject: Optional subject for the message
            
        Returns:
            SNS response containing MessageId and other metadata
        """
        return await self.publish_message(
            message=text,
            message_type=message_type,
            content_type="text/plain",
            topic_arn=topic_arn,
            subject=subject
        )
    
    async def publish_json_message(self, 
                              data: Dict[str, Any],
                              message_type: str = "template",
                              topic_arn: str = None,
                              subject: str = None) -> Dict[str, Any]:
        """
        Publish a JSON message to an SNS topic.
        
        Args:
            data: The dictionary to publish as JSON
            message_type: Value for the Message-Type attribute (defaults to "template")
            topic_arn: Optional override for the topic ARN
            subject: Optional subject for the message
            
        Returns:
            SNS response containing MessageId and other metadata
        """
        return await self.publish_message(
            message=data,
            message_type=message_type,
            content_type="application/json",
            topic_arn=topic_arn,
            subject=subject
        )


async def example_usage():
    """Example of how to use the SNSClient."""
    # Define the SNS topic ARN
    topic_arn = "arn:aws:sns:ap-southeast-2:343218181976:template-sns"
    
    # Create a client with explicit configuration
    async with SNSClient(topic_arn=topic_arn) as sns_client:
        # Example 1: Publish a JSON message
        json_response = await sns_client.publish_json_message(
            data={"abc": "abc"}
        )
        
        # Example 2: Publish a plain text message
        text_response = await sns_client.publish_text_message(
            text="Hello, this is a plain text message"
        )
        
        # Example 3: Using the general publish_message method with a subject
        default_response = await sns_client.publish_message(
            message={"data": "Using general method"},
            subject="Example message notification"
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage()) 