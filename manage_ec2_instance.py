#!/usr/bin/python
import sys, getopt
import boto3
import functions as f
from key_manage import Keys


def main(argv):
    keys = Keys()
    _access_key = keys._access_key
    _secret_access_key = keys._secret_access_key

    _region = 'eu-west-1'

    try:
        opts, args = getopt.getopt(argv, "hi:o:i", [
            "option=",
            "instance="])
    except getopt.GetoptError:
        print(
            'manage_ec2_instance.py -o <option(create_instance|get_instances|stop_instances|'
            'start_instances|terminate_instances|get_instance)> -i <instance>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'manage_ec2_instance.py -o <option(create_instance|get_instances|stop_instances|'
                'start_instances|terminate_instances|get_instance)> -i <instance>')
            sys.exit()

        elif opt in ("-o", "--option"):
            option = arg

        elif opt in ("-i", "--instance"):
            instance_id = arg

    ec2_client = boto3.client('ec2',
                              aws_access_key_id=_access_key,
                              aws_secret_access_key=_secret_access_key,
                              region_name=_region
                              )
    ec2_resource = boto3.resource('ec2',
                                  aws_access_key_id=_access_key,
                                  aws_secret_access_key=_secret_access_key,
                                  region_name=_region
                                  )

    if option == 'create_ec2':
        f.create_instance(ec2_client)

    if option == 'get_instances':
        f.get_instances(ec2_client, 'opensouth')

    if option == 'stop_instances':
        _instances_id = f.get_instances(ec2_client, 'opensouth')

        f.stop_instances(ec2_client, _instances_id)
        _instances_id = f.get_instances(ec2_client, 'opensouth')

    if option == 'start_instances':
        _instances_id = f.get_instances(ec2_client, 'opensouth')

        f.start_instances(ec2_client, _instances_id)
        _instances_id = f.get_instances(ec2_client, 'opensouth')

    if option == 'terminate_instances':
        _instances_id = f.get_instances(ec2_client, 'opensouth')

        f.terminate_instances(ec2_client, _instances_id)
        _instances_id = f.get_instances(ec2_client, 'opensouth')

    if option == 'get_instance':
        f.get_instance_status(ec2_resource, instance_id)


if __name__ == "__main__":
    main(sys.argv[1:])
