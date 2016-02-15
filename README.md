AWS Route53
===============
This will add AWS EC2 machines into Route53 creating a Health Check and a DNS record for the host.  You can run
this on the command line or add it into Lambda listening to auto scaling events to trigger an automatic add.

## Setting up your environment

Setup virtualenv

    virtualenv venv
    source venv/bin/activate

Install dependencies

    python setup.py install

Run the unit test

    nosetests

#### AWS Credentials
There are two ways to give it the AWS keys

1) Create a file in `~/.aws/credentials` with the content:

     [default]
     aws_access_key_id = <aws_key>
     aws_secret_access_key = <aws_secret>

2) Export the keys to the enviornment like:

     export AWS_ACCESS_KEY_ID=
     export AWS_SECRET_ACCESS_KEY=
     export AWS_DEFAULT_REGION=us-east-1

## Setup Machines DNS

* Setup Health Checks
* Setup DNS records

Procedure:
1. Given the SNS info, get the ec2 instance ID
1. Query for this instance info
1. Setup health checks to the default PublicDnsName
1. Setup the weight DNS record

### Usage

Adding:

     python worker_scaling_event_dns.py --ec2-instance-id i-88b1eb01 --event-type 'autoscaling:EC2_INSTANCE_LAUNCH'

Deleting:

     python worker_scaling_event_dns.py --ec2-instance-id i-88b1eb01 --event-type 'autoscaling:EC2_INSTANCE_TERMINATE'

### Launch SNS Message:

      {
          "StatusCode": "InProgress",
          "Service": "AWS Auto Scaling",
          "AutoScalingGroupName": "kube-prod1-slave-external-b-AutoScalingGroupCoreOSKubeNodesZone1-1UC4JZGJNI7R2",
          "Description": "Launching a new EC2 instance: i-db11935b",
          "ActivityId": "96f7be55-0f5d-4fa5-b3c6-f86a3387b497",
          "Event": "autoscaling:EC2_INSTANCE_LAUNCH",
          "Details": {
            "Availability Zone": "us-east-1b",
            "Subnet ID": "subnet-926a32b9"
          },
          "AutoScalingGroupARN": "arn:aws:autoscaling:us-east-1:320005014399:autoScalingGroup:26097f18-c267-4837-98f2-c9885b7e89af:autoScalingGroupName/kube-prod1-slave-external-b-AutoScalingGroupCoreOSKubeNodesZone1-1UC4JZGJNI7R2",
          "Progress": 50,
          "Time": "2016-02-05T00:52:44.550Z",
          "AccountId": "320005014399",
          "RequestId": "96f7be55-0f5d-4fa5-b3c6-f86a3387b497",
          "StatusMessage": "",
          "EndTime": "2016-02-05T00:52:44.550Z",
          "EC2InstanceId": "i-db11935b",
          "StartTime": "2016-02-05T00:51:40.385Z",
          "Cause": "At 2016-02-05T00:51:16Z a user request update of AutoScalingGroup constraints to min: 2, max: 2, desired: 2 changing the desired capacity from 1 to 2.  At 2016-02-05T00:51:38Z an instance was started in response to a difference between desired and actual capacity, increasing the capacity from 1 to 2."
        }

### Terminate SNS Message:

    {
      "StatusCode": "InProgress",
      "Service": "AWS Auto Scaling",
      "AutoScalingGroupName": "kube-prod1-slave-external-b-AutoScalingGroupCoreOSKubeNodesZone1-1UC4JZGJNI7R2",
      "Description": "Terminating EC2 instance: i-4c76f4cc",
      "ActivityId": "94ea9ffa-b363-4bdd-b152-b5c917ba8b8a",
      "Event": "autoscaling:EC2_INSTANCE_TERMINATE",
      "Details": {
        "Availability Zone": "us-east-1b",
        "Subnet ID": "subnet-926a32b9"
      },
      "AutoScalingGroupARN": "arn:aws:autoscaling:us-east-1:320005014399:autoScalingGroup:26097f18-c267-4837-98f2-c9885b7e89af:autoScalingGroupName/kube-prod1-slave-external-b-AutoScalingGroupCoreOSKubeNodesZone1-1UC4JZGJNI7R2",
      "Progress": 50,
      "Time": "2016-02-05T00:50:17.887Z",
      "AccountId": "320005014399",
      "RequestId": "94ea9ffa-b363-4bdd-b152-b5c917ba8b8a",
      "StatusMessage": "",
      "EndTime": "2016-02-05T00:50:17.887Z",
      "EC2InstanceId": "i-4c76f4cc",
      "StartTime": "2016-02-05T00:49:08.000Z",
      "Cause": "At 2016-02-05T00:48:38Z a user request update of AutoScalingGroup constraints to min: 1, max: 1, desired: 1 changing the desired capacity from 2 to 1.  At 2016-02-05T00:49:07Z an instance was taken out of service in response to a difference between desired and actual capacity, shrinking the capacity from 2 to 1.  At 2016-02-05T00:49:08Z instance i-4c76f4cc was selected for termination."
    }

## AWS Lambda Setup

You will need to create an AWS Lambda function. 

### Lambda Settings

* Point the Handler to `worker_scaling_event_dns.lambda_handler`
* Memory 128MB
* Timeout 30 sec
* Role

        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": "arn:aws:logs:*:*:*"
                },
                {
                    "Sid": "Stmt1454995642000",
                    "Effect": "Allow",
                    "Action": [
                        "ec2:*"
                    ],
                    "Resource": [
                        "*"
                    ]
                },
                {
                    "Sid": "Stmt1454995661000",
                    "Effect": "Allow",
                    "Action": [
                        "route53:*"
                    ],
                    "Resource": [
                        "*"
                    ]
                }
            ]
        }

### Packaging this app as a zip for Lambda

Doc:  http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

* Add third party packages to the root of the directory

        pip install configparser -t .

* Add all the zip files to a zip

        zip -r9 ~/Downloads/kube-route53-package.zip *

## Todo:

* Instead of putting the instance-public-ip into the health checks tags.  We should change the lifecycle policy for the
instance to be in standby, then we can take action on it:  https://aws.amazon.com/blogs/aws/auto-scaling-update-lifecycle-standby-detach/

