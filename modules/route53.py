import boto3
import logging
import random

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

class Route53:
    """

    """

    def __init__(self):
        """

        :return:
        """

        self.client = boto3.client('route53')
        self.hosted_zone_id = ''

    def set_hosted_zone_id(self, string):
        self.hosted_zone_id = string

    def create_resource_record_sets(self, action, resource_record_set_dict, comment):
        """
        Doc: http://boto3.readthedocs.org/en/latest/reference/services/route53.html#Route53.Client.change_resource_record_sets

        :return:
        """

        response = self.client.change_resource_record_sets(
            HostedZoneId=self.hosted_zone_id,
            ChangeBatch={
                'Comment': comment,
                'Changes': [
                    {
                        'Action': action,
                        'ResourceRecordSet': resource_record_set_dict
                    },
                ]
            }
        )

        return response

    def create_health_check(self, health_check_config_dict):
        """
        Doc: http://boto3.readthedocs.org/en/latest/reference/services/route53.html#Route53.Client.create_health_check

        :return:
        """

        caller_reference = 'aws-route53-updater'+str(random.randrange(100000, 999999999))

        response = self.client.create_health_check(
            CallerReference=caller_reference,
            HealthCheckConfig=health_check_config_dict
        )

        return response

    def delete_health_check(self, health_check_id):
        """

        :return:
        """

        response = self.client.delete_health_check(
            HealthCheckId=health_check_id
        )

        return response

    def change_tags_for_resource_health_check(self, health_check_id, key, value):
        """
        Adds a tag for a health check.  So we can find it easier later

        Doc: http://boto3.readthedocs.org/en/latest/reference/services/route53.html#Route53.Client.change_tags_for_resource

        :param health_check_id:
        :param ec2_instance_id:
        :return:
        """

        response = self.client.change_tags_for_resource(
                    ResourceType='healthcheck',
                    ResourceId=health_check_id,
                    AddTags=[
                        {
                            'Key': key,
                            'Value': value
                        },
                    ]
                )

        return response




