import argparse
import logging
import json
import configparser
import modules.route53
import modules.ec2

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--event-type", nargs="?", default="autoscaling:EC2_INSTANCE_LAUNCH", dest="event_type",
       help="The event type, launch or terminate.  Defaults to autoscaling:EC2_INSTANCE_LAUNCH")
    parser.add_argument("-e", "--ec2-instance-id", nargs="?", default="i-db11935b", dest="ec2_instance_id",
       help="The ec2 instance to work on.")

    return parser.parse_args()

def lambda_handler(event, context):
    """
    Execute this on AWS Lambda.  This is the entry point for Lambda and for it to pass in params.

    :param event:
    :param context:
    :return:
    """
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info('got event: {}'.format(event))
    logging.info('got context: {}'.format(context))

    # Location of the SNS message
    logging.info("XXXXXX")
    #logging.info(event['Records'][0]['Sns']['Message'])

    sns_message_dict = json.loads(event['Records'][0]['Sns']['Message'])
    logging.info(json.loads(event['Records'][0]['Sns']['Message']))

    logging.info("EC2 Instance: "+sns_message_dict['EC2InstanceId'])

    event_type = sns_message_dict['Event']

    main(event_type, sns_message_dict['EC2InstanceId'])

    return False

def main(event_type, ec2_instance_id):
    """
    Main function for this worker no matter what the entry point is (Lambda, CLI)

    :return:
    """

    if event_type == "autoscaling:EC2_INSTANCE_LAUNCH":
        ec2_launch_event(ec2_instance_id)
    if event_type == "autoscaling:EC2_INSTANCE_TERMINATE":
        ec2_terminate_event(ec2_instance_id)


def ec2_launch_event(ec2_instance_id):
    """
    When an ec2 instance launches it will add the health checks and dns records for the node

    """

    # config
    settings = configparser.ConfigParser()
    settings.read('config.ini')

    logging.info("Event: ec2_launch_event")
    logging.info("Working on ec2-instance id: "+ec2_instance_id)
    logging.info("Using route53 hosted zone id: "+settings.get('route53', 'hosted_zone'))
    logging.info("Domain name: "+settings.get('route53', 'domain_name'))

    # Get instance information
    ec2 = modules.ec2.Ec2()

    response_ec2_describe = ec2.describe_instances(ec2_instance_id)

    logging.debug(response_ec2_describe)

    logging.info("Instance public dns: "+response_ec2_describe['Reservations'][0]['Instances'][0]['PublicDnsName'])
    logging.info("Instance public IP: "+response_ec2_describe['Reservations'][0]['Instances'][0]['PublicIpAddress'])

    # Filter on the machine_filter config value to determine if we want to add this machine into the DNS
    machine_tag_value = ec2.get_tag_from_describe_instance_response(response_ec2_describe,
                                                                    settings.get('machine_filter', 'ec2_tag_key'))

    if settings.get('machine_filter', 'ec2_tag_value') == machine_tag_value:

        logging.info("This machine passes the machine_filter.  Add to DNS. "+machine_tag_value)

        # init route53 object
        route53 = modules.route53.Route53()

        health_check_config_dict = {
                    'Port': int(settings.get('health_check', 'port')),
                    'Type': settings.get('health_check', 'protocol_type'),
                    'ResourcePath': settings.get('health_check', 'ResourcePath'),
                    'FullyQualifiedDomainName': response_ec2_describe['Reservations'][0]['Instances'][0]['PublicDnsName'],
                    'RequestInterval': int(settings.get('health_check', 'RequestInterval')),
                    'FailureThreshold': int(settings.get('health_check', 'FailureThreshold')),
                }

        response_create_health_check = route53.create_health_check(health_check_config_dict)

        logging.debug(response_create_health_check)

        logging.info("Health check id: "+response_create_health_check['HealthCheck']['Id'])

        # Add tag for health check
        response = route53.change_tags_for_resource_health_check(response_create_health_check['HealthCheck']['Id'],
                                                                 'Name', settings.get('health_check', 'name'))
        response = route53.change_tags_for_resource_health_check(response_create_health_check['HealthCheck']['Id'],
                                                                 'instance-id', ec2_instance_id)

        # Create DNS record object
        route53.set_hosted_zone_id(settings.get('route53', 'hosted_zone'))

        # Add DNS record
        resource_record_set_dict = {
                                    'Name': ec2_instance_id+'.'+settings.get('route53', 'domain_name'),
                                    'Type': settings.get('dns_record_set', 'type'),
                                    'SetIdentifier': ec2_instance_id,
                                    'Weight': int(settings.get('dns_record_set', 'Weight')),
                                    'TTL': int(settings.get('dns_record_set', 'TTL')),
                                    'ResourceRecords': [
                                        {
                                            'Value': response_ec2_describe['Reservations'][0]['Instances'][0]['PublicIpAddress']
                                        },
                                    ],
                                    'HealthCheckId': response_create_health_check['HealthCheck']['Id']
                                }

        response_create_resource_record_sets = route53.create_resource_record_sets('UPSERT',
                                                                                   resource_record_set_dict,
                                                                                   settings.get('dns_record_set', 'comment'))

        logging.debug(response_create_resource_record_sets)

    else:
        logging.info("This machine is not part of the machine_filter. Not adding to DNS. "+machine_tag_value)

def ec2_terminate_event(ec2_instance_id):
    """
    When an ec2 instance is terminated, the DNS record and health check for this server is removed

    """

    # config
    settings = configparser.ConfigParser()
    settings.read('config.ini')

    logging.info("Event: ec2_termination_event")
    logging.info("Working on ec2-instance id: "+ec2_instance_id)
    logging.info("Using route53 hosted zone id: "+settings.get('route53', 'hosted_zone'))
    logging.info("Domain name: "+settings.get('route53', 'domain_name'))

    # Get instance information
    ec2 = modules.ec2.Ec2()

    response_ec2_describe = ec2.describe_instances(ec2_instance_id)

    logging.info("Instance public dns: "+response_ec2_describe['Reservations'][0]['Instances'][0]['PublicDnsName'])
    logging.info("Instance public IP: "+response_ec2_describe['Reservations'][0]['Instances'][0]['PublicIpAddress'])

    # init route53 object
    route53 = modules.route53.Route53()
    route53.set_hosted_zone_id(settings.get('route53', 'hosted_zone'))

    health_check_id = route53.get_health_check_by_tag('instance-id', ec2_instance_id)

    # Delete DNS record
    resource_record_set_dict = {
                                'Name': ec2_instance_id+'.'+settings.get('route53', 'domain_name'),
                                'Type': settings.get('dns_record_set', 'type'),
                                'SetIdentifier': ec2_instance_id,
                                'Weight': int(settings.get('dns_record_set', 'Weight')),
                                'TTL': int(settings.get('dns_record_set', 'TTL')),
                                'ResourceRecords': [
                                    {
                                        'Value': response_ec2_describe['Reservations'][0]['Instances'][0]['PublicIpAddress']
                                    },
                                ],
                                'HealthCheckId': health_check_id
                            }

    logging.debug(resource_record_set_dict)

    try:
        response_delete_resource_record_sets = route53.create_resource_record_sets('DELETE', resource_record_set_dict, '')

        logging.debug(response_delete_resource_record_sets)
    except:
        logging.info("Unable to delete the record set")
        logging.info(resource_record_set_dict)


    # Search for health check via tag
    searched_health_check_id = route53.get_health_check_by_tag('instance-id', ec2_instance_id)

    # Delete health check
    try:
        delete_response = route53.delete_health_check(searched_health_check_id)
    except:
        logging.info("Unable to delete the health check")

if __name__ == "__main__":
    """
    Mainly for running from the CLI.

    """

    args = parseArgs()

    main(args.event_type, args.ec2_instance_id)


