#!/usr/bin/python
import sys, getopt
import boto3
import functions as f
from key_manage import Keys
import json

def main(argv):
    keys = Keys()
    _access_key = keys._access_key
    _secret_access_key = keys._secret_access_key
    _region = 'eu-west-1'

    try:
        opts, args = getopt.getopt(argv, "hi:o:a", ["option=","arn="])
    except getopt.GetoptError:
        print('manace_ec2.py -o <option> -a <arn>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -o <option> -a <arn>')
            sys.exit()

        elif opt in ("-o", "--option"):
            option = arg

        elif opt in ("-a", "--arn"):
            arn = arg

    iam_client = boto3.client('iam',
                                 aws_access_key_id=_access_key,
                                 aws_secret_access_key=_secret_access_key,
                                 region_name=_region
                                 )

    if option == 'create_policy':
        f.create_policy(iam_client)
    if option == 'create_policy_file':

        with open('policy.txt') as json_file:
            data = json.load(json_file)

        print(data)
        f.create_policy(iam_client,data)

    if option == 'add_policy_to_user':
        user_name = 'opensouth'
        arn_policy = 'arn:aws:iam::223876296831:policy/opensouth_policy_test'
        f.add_policy_to_user(iam_client, user_name, arn_policy)

    if option == 'remove_policy_to_user':
        user_name = 'opensouth'
        arn_policy = 'arn:aws:iam::223876296831:policy/opensouth_policy_test'
        f.remove_policy_user(iam_client, user_name, arn_policy)

    if option == 'add_to_user':
        user_name = 'opensouth'
        print(arn)
        print(user_name)

        f.add_policy_to_user(iam_client, user_name, arn)




if __name__ == "__main__":
    main(sys.argv[1:])
