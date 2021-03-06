#!/usr/bin/env python3
import boto3
import logging

logging.basicConfig(level=20, format='%(asctime)s: %(name)s | LOG: %(message)s')
log = logging.getLogger(__name__)

class ParameterHandler:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value
    
    def find(self):
        log.info('Running: Parameter.find')

        ssm = boto3.client('ssm')
        res = ssm.describe_parameters(Filters=[{'Key': (self.tag),'Values': [self.value]}])

        try:
            ssm_info = {
                'Name': res['Parameters'][0]['Name']['Name']
            }
            
        except IndexError as e:
            log.info('Cannot Find Parameter')
            return False

        return ssm_info

class InstanceHandler:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

    def find(self):
        log.info('Running: InstanceHandler.find')

        ec2 = boto3.client('ec2')
        res = ec2.describe_instances(Filters=[{'Name': ('tag:'+self.tag),'Values': [self.value]}])

        try:
            instance_state = res['Reservations'][0]['Instances'][0]['State']['Name']

            try:
                instance_id = res['Reservations'][0]['Instances'][0]['InstanceId']
            except:
                instance_id = 'null'
            try:
                private_ip = res['Reservations'][0]['Instances'][0]['PrivateIpAddress']
            except:
                private_ip = 'null'
            try:
                public_ip = res['Reservations'][0]['Instances'][0]['PublicIpAddress']
            except:
                public_ip = 'null'

            instanceinfo = {
                'InstanceID': instance_id,
                'InstancePrivateIP': private_ip,
                'InstanceIP': public_ip,
                'InstanceState': instance_state
            }

        except IndexError as e:
            log.info('Cannot Find Instance')
            return False

        return instanceinfo

    def start(self):
        log.info('Running: InstanceHandler.start')

        ec2 = boto3.client('ec2')
        res = ec2.describe_instances(Filters=[{'Name': ('tag:'+self.tag),'Values': [self.value]}])

        try:
            ec2.start_instances(InstanceIds=[res['Reservations'][0]['Instances'][0]['InstanceId']])

        except IndexError as e:
            log.info('Cannot Find Instance')
            return False


        return True

    def stop(self):
        log.info('Running: InstanceHandler.stop')

        ec2 = boto3.client('ec2')
        res = ec2.describe_instances(Filters=[{'Name': ('tag:'+self.tag),'Values': [self.value]}])

        try:
            ec2.stop_instances(InstanceIds=[res['Reservations'][0]['Instances'][0]['InstanceId']])

        except IndexError as e:
            log.info('Cannot Find Instance')
            return False

        return True