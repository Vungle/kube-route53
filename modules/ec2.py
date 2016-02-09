import boto3
import logging

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

class Ec2:
    """

    """

    def __init__(self):
        """

        :return:
        """

        self.client = boto3.client('ec2')


    def describe_instances(self, instance_id):
        """

        :param instance_id:
        :return:
        """

        response = self.client.describe_instances(
            DryRun=False,
            InstanceIds=[
                instance_id
            ]
        )

        return response

    def get_tag_from_describe_instance_response(self, describe_instances_response, tag_key):
        """
        This function will take in the response from describe_instances and return the value for the
        tag_key parameter.

        We need to do this b/c the tags comes back in a numbered array and we have to loop through it
        to find the key.

        :param describe_instances_response:
        :param tag_key:
        :return:
        """

        tag_value = None

        logging.debug(describe_instances_response['Reservations'][0]['Instances'][0]['Tags'])

        for item in describe_instances_response['Reservations'][0]['Instances'][0]['Tags']:
            if item['Key'] == tag_key:
                tag_value = item['Value']

        return tag_value


