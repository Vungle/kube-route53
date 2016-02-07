import boto3
import logging

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

# queue documentation: https://boto3.readthedocs.org/en/latest/guide/sqs.html#sqs
# queue api documentation: http://boto3.readthedocs.org/en/latest/reference/services/sqs.html#SQS.Client.delete_queue
# Class message:  https://boto3.readthedocs.org/en/latest/reference/services/sqs.html#message
    # This is what the queue returns


def send_a_message(queue_name, message):

    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    # Create a new message
    response = queue.send_message(MessageBody=message)

    # The response is NOT a resource, but gives you a message ID and MD5
    logging.debug(response.get('MessageId'))
    logging.debug(response.get('MD5OfMessageBody'))

# Get one message from a queue
def get_one_message(queue_name, visibility_timeout=30):

    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MaxNumberOfMessages=1, VisibilityTimeout=visibility_timeout):

        # Print out the body and author (if set)
        logging.debug('Message: {0}'.format(message.body))

        # Let the queue know that the message is processed
        #message.delete()

        # return the first message if found and end the loop
        return message

def change_message_visibility(message_obj, visibility_timeout):

    logging.debug("Changing message visibility to: "+str(visibility_timeout))

    message_obj.change_visibility(VisibilityTimeout=visibility_timeout)

def delete_a_message(message_obj):

    try:
        message_obj.delete()
    except:
        logging.error("Fail to delete queue object.")

def create_a_queue(queue_name):

    # Get the service resource
    sqs = boto3.resource('sqs')

    # Create the queue. This returns an SQS.Queue instance
    queue = sqs.create_queue(QueueName=queue_name, Attributes={'DelaySeconds': '5'})

    # You can now access identifiers and attributes
    logging.debug(queue.url)
    logging.debug(queue.attributes.get('DelaySeconds'))

    return queue.url

def delete_a_queue(queue_url):

    # Get the service resource
    sqs = boto3.resource('sqs')

    sqs.delete_queue(QueueUrl=queue_url)


