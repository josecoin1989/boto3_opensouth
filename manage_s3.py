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
        opts, args = getopt.getopt(argv, "hi:o:",
                                   ["option= create_bucket|upload_file|delete_file|download_file|get_files", ])
    except getopt.GetoptError:
        print('manace_ec2.py -o <option> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -o <option> ')
            sys.exit()

        elif opt in ("-o", "--option"):
            option = arg

        s3_client = boto3.client('s3',
                                 aws_access_key_id=_access_key,
                                 aws_secret_access_key=_secret_access_key,
                                 region_name=_region
                                 )

    if option == 'create_bucket':
        f.create_bucket(s3_client)

    if option == 'upload_file':
        f.upload_file(s3_client=s3_client, file='boto3.jpg', bucket='opensouthtest')

    if option == 'delete_file':
        f.delete_file(s3_client=s3_client, file='boto3.jpg', bucket='opensouthtest')

    if option == 'download_file':
        f.download_file(s3_client=s3_client, file='boto3.jpg', bucket='opensouthtest')

    if option == 'get_files':
        f.get_files(s3_client=s3_client, bucket='opensouthtest')


if __name__ == "__main__":
    main(sys.argv[1:])
