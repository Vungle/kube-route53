import unittest
import modules.route53
import time
import random

class Route53Test(unittest.TestCase):
    """

    """

    def delete_health_check(self, health_check_id):
        """

        :return:
        """

        route53 = modules.route53.Route53()

        route53.delete_health_check(health_check_id)


    def test_create_record_set(self):
        """
        Creates or updates a record if it is already there with the new values

        :return:
        """

        hosted_zone_id = 'Z1UNV9CC0W9AR7' # Unit testing zone in the vungle2 account
        zone_domain = 'unit-test-zone.com'
        hostname = 'test-unittest'

        comment = 'unit test record'

        route53 = modules.route53.Route53()
        route53.set_hosted_zone_id(hosted_zone_id)

        resource_record_set_dict = {
                                'Name': hostname+'.'+zone_domain,
                                'Type': 'A',
                                'SetIdentifier': '1111',
                                'Weight': 10,
                                'TTL': 15,
                                'ResourceRecords': [
                                    {
                                        'Value': '1.1.1.1'
                                    },
                                ],
                                'HealthCheckId': 'a29a5665-7bea-47b2-b977-b56b45301a6e'
                            }

        response = route53.create_resource_record_sets('UPSERT', resource_record_set_dict, comment)

        #print "XXXXX"
        #print response['ChangeInfo']['Status']
        #print response

        self.assertEqual(response['ChangeInfo']['Comment'], comment)

    def test_create_and_delete_record_set(self):
        """
        Creates then deletes a DNS record set

        :return:
        """

        hosted_zone_id = 'Z1UNV9CC0W9AR7' # Unit testing zone in the vungle2 account
        zone_domain = 'unit-test-zone.com'
        hostname = 'test-unittest'

        comment = 'unit test record'

        route53 = modules.route53.Route53()
        route53.set_hosted_zone_id(hosted_zone_id)

        resource_record_set_dict = {
                                'Name': hostname+'.'+zone_domain,
                                'Type': 'A',
                                'SetIdentifier': '2222',
                                'Weight': 10,
                                'TTL': 15,
                                'ResourceRecords': [
                                    {
                                        'Value': '2.2.2.2'
                                    }
                                ]
                            }

        # Create
        response = route53.create_resource_record_sets('UPSERT', resource_record_set_dict, comment)

        #print "XXXXX"
        #print response['ChangeInfo']['Status']
        #print response

        self.assertEqual(response['ChangeInfo']['Comment'], comment)

        # Delete - Need to match everything, including the HealthCheckId if it is there
        resource_record_set_dict = {
                                'Name': hostname+'.'+zone_domain+'.',
                                'Type': 'A',
                                'SetIdentifier': '2222',
                                'Weight': 10,
                                'TTL': 15,
                                'ResourceRecords': [
                                    {
                                        'Value': '2.2.2.2'
                                    }
                                ]
                            }

        response_delete = route53.create_resource_record_sets('DELETE', resource_record_set_dict, comment)

        print response_delete

        #self.assertEquals(1, 2)

    def test_create_health_check(self):
        """

        :return:
        """

        zone_domain = 'unit-test-zone.com'
        hostname = 'test-unittest'
        port = 80
        protocol_type = 'HTTP'

        route53 = modules.route53.Route53()

        health_check_config_dict = {
                'Port': port,
                'Type': protocol_type,
                'ResourcePath': '/',
                'FullyQualifiedDomainName': hostname+'.'+zone_domain,
                'RequestInterval': 10,
                'FailureThreshold': 3
            }

        # Create health check
        response = route53.create_health_check(health_check_config_dict)

        print "XXXXX Create"
        print response

        health_check_id = response['HealthCheck']['Id']
        #health_check_creation_status_code = response['ResponseMetadata']['HTTPStatusCode']

        self.assertEqual(response['HealthCheck']['HealthCheckConfig']['FullyQualifiedDomainName'], hostname+'.'+zone_domain)
        self.assertEquals(response['HealthCheck']['HealthCheckConfig']['ResourcePath'], '/')

        # Delete the health check
        time.sleep(.5)
        delete_response = self.delete_health_check(health_check_id)

        print "XXXXX Delete"
        print response

        self.assertEquals(delete_response, None)

        #self.assertEquals(1, 2)

    def test_create_and_delete_health_check(self):
        """
        Will create, tag health check, search for it via a tag, then delete it.

        :return:
        """

        zone_domain = 'unit-test-zone.com'
        hostname = 'test-unittest'
        port = 80
        protocol_type = 'HTTP'

        route53 = modules.route53.Route53()

        health_check_config_dict = {
                'Port': port,
                'Type': protocol_type,
                'ResourcePath': '/',
                'FullyQualifiedDomainName': hostname+'.'+zone_domain,
                'RequestInterval': 10,
                'FailureThreshold': 3
            }

        # Create health check
        response = route53.create_health_check(health_check_config_dict)

        print "XXXXX Create"
        print response

        self.assertEqual(response['HealthCheck']['HealthCheckConfig']['FullyQualifiedDomainName'], hostname+'.'+zone_domain)
        self.assertEquals(response['HealthCheck']['HealthCheckConfig']['ResourcePath'], '/')

        health_check_id = response['HealthCheck']['Id']
        #health_check_creation_status_code = response['ResponseMetadata']['HTTPStatusCode']

        # Tag health check
        tag_name = 'unit-test-name'
        tag_value = 'test_create_and_delete_health_check-'+str(random.randrange(100000, 999999999))
        route53.change_tags_for_resource_health_check(health_check_id, 'Name', 'unit-test')
        route53.change_tags_for_resource_health_check(health_check_id, tag_name, tag_value)

        # Search for health check via tag
        searched_health_check_id = route53.get_health_check_by_tag(tag_name, tag_value)

        self.assertEqual(health_check_id, searched_health_check_id)


        # Delete the health check
        time.sleep(.5)
        delete_response = self.delete_health_check(health_check_id)

        #print "XXXXX Delete"
        #print response

        self.assertEquals(delete_response, None)

        #self.assertEquals(1, 2)

