import json
import logging
from .handlers.template_handler import handle_template

# Get a logger for this module
logger = logging.getLogger(__name__)

# Add your handlers here
# The key is the message type
# The value is the handler function
route_table = {
    "template": handle_template,
}

async def route_message(message: dict, delete_unknown_types: bool = True) -> bool:
    """
    Route a message to the appropriate handler based on its type.
    
    Args:
        message: The SQS message to route
        delete_unknown_types: Whether to delete messages with unknown types
        
    Returns:
        bool: True if the message was successfully handled, False if not
    """
    # First, check if this is an SNS message wrapped in SQS
    body = message.get("Body", "")
    sns_message = None
    is_sns_message = False
    
    # Try to parse the body as JSON to see if it's an SNS message
    if body:
        try:
            parsed_body = json.loads(body)
            # Check if it has SNS-specific fields
            if isinstance(parsed_body, dict) and parsed_body.get("Type") == "Notification":
                is_sns_message = True
                sns_message = parsed_body
                logger.debug("Detected SNS message")
        except json.JSONDecodeError:
            # Not a JSON body, so not an SNS message
            pass
            
    if is_sns_message:
        # For SNS messages, the message attributes are in the parsed body
        sns_message_attributes = sns_message.get("MessageAttributes", {})
        
        # Extract message type and content type from SNS message attributes
        message_type = None
        content_type = None
        
        if "Message-Type" in sns_message_attributes:
            message_type = sns_message_attributes["Message-Type"].get("Value")
        elif "MessageType" in sns_message_attributes:
            message_type = sns_message_attributes["MessageType"].get("Value")
            
        if "Content-Type" in sns_message_attributes:
            content_type = sns_message_attributes["Content-Type"].get("Value")
        elif "ContentType" in sns_message_attributes:
            content_type = sns_message_attributes["ContentType"].get("Value")
        
        # The actual message content is in the "Message" field
        content = sns_message.get("Message", "")
        
        if content_type == "application/json" and content:
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON content for SNS message {sns_message.get('MessageId')}")
                return delete_unknown_types
    else:
        # Original SQS message handling
        message_attributes = message.get("MessageAttributes", {})
        
        message_type = message_attributes.get("Message-Type", {}).get("StringValue") if "Message-Type" in message_attributes else None
        content_type = message_attributes.get("Content-Type", {}).get("StringValue") if "Content-Type" in message_attributes else None
        
        # If message type is missing, try the old key format for backward compatibility
        if message_type is None:
            message_type = message_attributes.get("MessageType", {}).get("StringValue") if "MessageType" in message_attributes else None
            content_type = message_attributes.get("ContentType", {}).get("StringValue") if "ContentType" in message_attributes else None
        
        content = body
        if content_type == "application/json" and content:
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON content for message {message.get('MessageId')}")
                return delete_unknown_types
    
    if message_type is None:
        logger.warning(f"Message has no type attribute: {message.get('MessageId')}")
        return delete_unknown_types
    
    if message_type in route_table:
        try:
            await route_table[message_type](message, content)
            return True
        except Exception as e:
            logger.error(f"Error processing message of type {message_type}: {str(e)}")
            # Don't delete the message on processing error to allow retry
            return False
    else:
        logger.warning(f"Unknown message type: {message_type} for message {message.get('MessageId')}")
        # Delete unknown message types if configured to do so
        return delete_unknown_types
