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

        Used for: add, update, and delete

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
                    }
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

    def get_health_check_by_tag(self, key, value):
        """
        Retrieves a health check by the key and value

        Doc: http://boto3.readthedocs.org/en/latest/reference/services/route53.html#Route53.Client.list_health_checks

        :param key:
        :param value:
        :return:
        """

        resource_type = 'healthcheck'

        health_check_id = ''

        health_check_list = self.list_health_checks()

        #logging.debug((health_check_list))

        # For each of the health check, pull the tags for each ID
        for item in health_check_list['HealthChecks']:
            logging.debug(item['Id'])

            resource_tags = self.list_tags_for_resource(resource_type, item['Id'])

            logging.debug("resource_tags")
            logging.debug(resource_tags)

            # Loop through the tag list to see if we can find the key/value we want
            for a_tag in resource_tags['ResourceTagSet']['Tags']:
                if key == a_tag['Key'] and value == a_tag['Value']:
                    health_check_id = item['Id']

        return health_check_id

    def get_health_check_tag_value(self, ec2_instance_id, key):
        """
        Get a health check's tag with the given key

        :param health_check_id:
        :param key:
        :return:
        """

        resource_type = 'healthcheck'

        tag_value = ''

        health_check_list = self.list_health_checks()

        # For each of the health check, pull the tags for each ID
        for item in health_check_list['HealthChecks']:
            logging.debug(item['Id'])

            resource_tags = self.list_tags_for_resource(resource_type, item['Id'])

            logging.debug("resource_tags")
            logging.debug(resource_tags)

            # Loop through the tag list to see if we can find the key/value we want
            for a_tag in resource_tags['ResourceTagSet']['Tags']:

                if a_tag['Value'] == ec2_instance_id:
                    # This is the health check with the matching health check ID, look for the instance-public-ip

                    for a_tag2 in resource_tags['ResourceTagSet']['Tags']:
                        logging.debug(a_tag2['Key'])
                        logging.debug(a_tag2['Value'])
                        if a_tag2['Key'] == key:
                            tag_value = a_tag2['Value']

        return tag_value

    def list_health_checks(self):
        """
        Get a list of health checks

        :return:
        """

        # This will only grab the first hundred.  Have to implement paging for more than 100.
        response = self.client.list_health_checks()
               #     Marker='string',
               #     MaxItems='string'
               # )

        return response

    def list_tags_for_resource(self, resource_type, resource_id):
        """
        Gets the tags for a given resource_type and resource_id

        resource_type = 'healthcheck'|'hostedzone'

        Doc: http://boto3.readthedocs.org/en/latest/reference/services/route53.html#Route53.Client.list_tags_for_resource

        :param resource_id:
        :return:
        """

        response = self.client.list_tags_for_resource(
                    ResourceType=resource_type,
                    ResourceId=resource_id
                )

        return response








