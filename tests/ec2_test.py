import unittest
import modules.ec2
import pprint

class Ec2Test(unittest.TestCase):
    """

    """

    def test_describe_instances(self):
        """
        Creates or updates a record if it is already there with the new values

        response dictionary:

        {   u'Reservations': [   {   u'Groups': [],
                             u'Instances': [   {   u'AmiLaunchIndex': 0,
                                                   u'Architecture': 'x86_64',
                                                   u'BlockDeviceMappings': [   {   u'DeviceName': '/dev/xvda',
                                                                                   u'Ebs': {   u'AttachTime': datetime.datetime(2015, 9, 25, 6, 13, 9, tzinfo=tzutc()),
                                                                                               u'DeleteOnTermination': True,
                                                                                               u'Status': 'attached',
                                                                                               u'VolumeId': 'vol-94754379'}}],
                                                   u'ClientToken': 'kube-EC2In-F9IPK3NX0NDN',
                                                   u'EbsOptimized': False,
                                                   u'Hypervisor': 'xen',
                                                   u'ImageId': 'ami-303b1458',
                                                   u'InstanceId': 'i-96e7cf35',
                                                   u'InstanceType': 'c3.large',
                                                   u'KeyName': 'vungle-ops_2015-08-25',
                                                   u'LaunchTime': datetime.datetime(2015, 9, 25, 6, 13, 7, tzinfo=tzutc()),
                                                   u'Monitoring': {   u'State': 'disabled'},
                                                   u'NetworkInterfaces': [   {   u'Association': {   u'IpOwnerId': '320005014399',
                                                                                                     u'PublicDnsName': 'ec2-52-21-199-16.compute-1.amazonaws.com',
                                                                                                     u'PublicIp': '52.21.199.16'},
                                                                                 u'Attachment': {   u'AttachTime': datetime.datetime(2015, 9, 25, 6, 13, 7, tzinfo=tzutc()),
                                                                                                    u'AttachmentId': 'eni-attach-bad16fca',
                                                                                                    u'DeleteOnTermination': True,
                                                                                                    u'DeviceIndex': 0,
                                                                                                    u'Status': 'attached'},
                                                                                 u'Description': '',
                                                                                 u'Groups': [   {   u'GroupId': 'sg-12d7cc75',
                                                                                                    u'GroupName': 'kube-prod1-SecurityGroupNAT-1PKEIUX6430UJ'}],
                                                                                 u'MacAddress': '12:48:4d:55:b5:9d',
                                                                                 u'NetworkInterfaceId': 'eni-17c83636',
                                                                                 u'OwnerId': '320005014399',
                                                                                 u'PrivateDnsName': 'ip-172-16-11-64.ec2.internal',
                                                                                 u'PrivateIpAddress': '172.16.11.64',
                                                                                 u'PrivateIpAddresses': [   {   u'Association': {   u'IpOwnerId': '320005014399',
                                                                                                                                    u'PublicDnsName': 'ec2-52-21-199-16.compute-1.amazonaws.com',
                                                                                                                                    u'PublicIp': '52.21.199.16'},
                                                                                                                u'Primary': True,
                                                                                                                u'PrivateDnsName': 'ip-172-16-11-64.ec2.internal',
                                                                                                                u'PrivateIpAddress': '172.16.11.64'}],
                                                                                 u'SourceDestCheck': False,
                                                                                 u'Status': 'in-use',
                                                                                 u'SubnetId': 'subnet-926a32b9',
                                                                                 u'VpcId': 'vpc-cb72a6af'}],
                                                   u'Placement': {   u'AvailabilityZone': 'us-east-1b',
                                                                     u'GroupName': '',
                                                                     u'Tenancy': 'default'},
                                                   u'PrivateDnsName': 'ip-172-16-11-64.ec2.internal',
                                                   u'PrivateIpAddress': '172.16.11.64',
                                                   u'ProductCodes': [],
                                                   u'PublicDnsName': 'ec2-52-21-199-16.compute-1.amazonaws.com',
                                                   u'PublicIpAddress': '52.21.199.16',
                                                   u'RootDeviceName': '/dev/xvda',
                                                   u'RootDeviceType': 'ebs',
                                                   u'SecurityGroups': [   {   u'GroupId': 'sg-12d7cc75',
                                                                              u'GroupName': 'kube-prod1-SecurityGroupNAT-1PKEIUX6430UJ'}],
                                                   u'SourceDestCheck': False,
                                                   u'State': {   u'Code': 16,
                                                                 u'Name': 'running'},
                                                   u'StateTransitionReason': '',
                                                   u'SubnetId': 'subnet-926a32b9',
                                                   u'Tags': [   {   u'Key': 'aws:cloudformation:logical-id',
                                                                    u'Value': 'EC2InstanceNAT1a'},
                                                                {   u'Key': 'Name',
                                                                    u'Value': 'prod_NAT-1a'},
                                                                {   u'Key': 'EnvironmentName',
                                                                    u'Value': 'prod'},
                                                                {   u'Key': 'aws:cloudformation:stack-name',
                                                                    u'Value': 'kube-prod1'},
                                                                {   u'Key': 'aws:cloudformation:stack-id',
                                                                    u'Value': 'arn:aws:cloudformation:us-east-1:320005014399:stack/kube-prod1/5f0fbf40-634c-11e5-aa02-50fa5262a838'},
                                                                {   u'Key': 'CreatedFrom',
                                                                    u'Value': 'CloudFormation'},
                                                                {   u'Key': 'Functionality',
                                                                    u'Value': 'NAT Box in subnet 1'},
                                                                {   u'Key': 'KubernetesCluster',
                                                                    u'Value': 'kube-prod1'}],
                                                   u'VirtualizationType': 'hvm',
                                                   u'VpcId': 'vpc-cb72a6af'}],
                             u'OwnerId': '320005014399',
                             u'ReservationId': 'r-512f8387'}],
    'ResponseMetadata': {   'HTTPStatusCode': 200,
                            'RequestId': '74386d3d-ba1b-45a6-a916-30e86326f64d'}}

        :return:
        """
        pp = pprint.PrettyPrinter(indent=4)

        instance_id = 'i-96e7cf35' # This is the prod nat machine.  Assuming this will always be there

        ec2 = modules.ec2.Ec2()

        response = ec2.describe_instances(instance_id)

        print "XXXXXXX"
        print response

        pp.pprint(response)

        self.assertEquals(response['ResponseMetadata']['HTTPStatusCode'], 200)

        #self.assertEquals(1, 2)


