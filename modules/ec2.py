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

