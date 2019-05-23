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
                                   ["option= ", ])
    except getopt.GetoptError:
        print('manage_rds.py -o <option> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -o <option> ')
            sys.exit()

        elif opt in ("-o", "--option"):
            option = arg

        rds_client = boto3.client('rds',
                                 aws_access_key_id=_access_key,
                                 aws_secret_access_key=_secret_access_key,
                                 region_name=_region
                                 )

    rds_data = {'postgres': {
        'name': 'dbpro-postgres-opensouthtest' ,
        'type': 'db.m4.2xlarge',
        'engine': 'postgres',
        'engine_version': '10.6',
        'license': 'postgresql-license',
        'user_name': 'opensouthtest',
        'pw': 'opensouthtest',
        'database': 'opensouthtest',
        'volume': 5,
        'db_parameter_group_name': 'pg-rds-pro'
    },
        'mssql': {
            'name': 'dbpro-mssql-opensouthtest' ,
            'type': 'db.m4.2xlarge',
            'engine': 'sqlserver-se',
            'engine_version': '14.00.3035.2.v1',
            'user_name': 'opensouthtest',
            'pw': 'opensouthtest',
            'database': 'opensouthtest',
            'volume': 5,
            'db_parameter_group_name': 'pg-sqlserver-dq-ssl'
        }
    }

    if option == 'create_postgres':

        rds_data = {'postgres': {
            'name': 'opensouth-test',
            'type': 'db.m4.2xlarge',
            'engine': 'postgres',
            'engine_version': '10.6',
            'license': 'postgresql-license',
            'user_name': 'zbxadminpro',
            'pw': 'admin',
            'database': 'opensouth',
            'volume': 1,
            'db_parameter_group_name': 'pg-rds-pro'
        }
        }
        f.create_rds(rds_client)



if __name__ == "__main__":
    main(sys.argv[1:])
