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
        opts, args = getopt.getopt(argv, "hi:o:", ["option=", ])
    except getopt.GetoptError:
        print('manace_ec2.py -o <option> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -o <option> ' )
            sys.exit()

        elif opt in ("-o", "--option"):
            option = arg



        lambda_client = boto3.client('lambda',
                                     aws_access_key_id=_access_key,
                                     aws_secret_access_key=_secret_access_key,
                                     region_name=_region
                                     )

    if option == 'get_lambdas':
        f.get_lambdas(lambda_client)

    if option == 'invoke_lambda':
        _lambda = 'openstartec2'
        data = json.dumps({'instance_id': 'i-06cbe76c5a3ae3d51'})

        f.invoke_lambda(lambda_client, _lambda, data)


if __name__ == "__main__":
    main(sys.argv[1:])
