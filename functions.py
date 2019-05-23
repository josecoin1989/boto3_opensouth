import json


def create_instance(ec2_client):
    response = ec2_client.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 16,
                    'VolumeType': 'gp2'
                },
            },
        ],
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        ImageId='ami-030dbca661d402413',
        Monitoring={
            'Enabled': False
        },
        KeyName='opensouth_key',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'opensouth'
                    },
                ]
            },
        ],
    )

    print('Ec2 created')


def get_instances(ec2_client, name_filter):
    _filter = [{
        'Name': 'tag:Name',
        'Values': [
            name_filter,
        ]
    },
    ]

    _instances = ec2_client.describe_instances(Filters=_filter)['Reservations'][0]['Instances']

    _instances_id = []
    for i in _instances:
        print('Instance Id: ' + i['InstanceId'] + '\t| Instance Status:' + i['State']['Name'])
        _instances_id.append(i['InstanceId'])

    return _instances_id


def stop_instances(ec2_client, _instances_id):
    """
    Función para apagar una instancia
    :param ec2_client:
    :param _instances_id:
    :return:
    """
    ec2_client.stop_instances(InstanceIds=_instances_id)


def start_instances(ec2_client, _instances_id):
    """
    Función para encender una instancia
    :param ec2_client:
    :param _instances_id:
    :return:
    """
    ec2_client.start_instances(InstanceIds=_instances_id)


def terminate_instances(ec2_client, _instances_id):
    """
    Función para borrar una instancia
    :param ec2_client:
    :param _instances_id:
    :return:
    """
    ec2_client.terminate_instances(InstanceIds=_instances_id)


def get_instance_status(ec2_resource, _instance_id):
    """
    Función para obneter información de una instancia
    :param ec2_resource:
    :param _instance_id:
    :return:
    """
    instance = ec2_resource.Instance(_instance_id)

    print('Tags:' + str(instance.tags))
    print('Arquitectura: ' + instance.architecture)
    print('Status: ' + str(instance.state['Name']))


def create_policy(iam_client, data=None):
    """
    Función para permitir crear una policy por defecto ListFunctions, sino coge la policy recibida por
    parametros
    :param iam_client:
    :param data:
    :return:
    """
    if data is None:
        _policy = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Stmt1558416850250",
                    "Action": [
                        "lambda:ListFunctions"
                    ],
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ]
        })
        name = 'opensouth_policy_file'
    else:
        _policy = json.dumps(data)
        name = 'opensouth_policy'

    response = iam_client.create_policy(
        PolicyName=name,
        PolicyDocument=_policy,
        Description='Test Policy for opensouth_test'
    )

    print(response)


def add_policy_to_user(iam_client, user_name, arn_policy):
    """
    Agrega una policy a un usuario
    :param iam_client:
    :param user_name:
    :param arn_policy:
    :return:
    """
    response = iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=arn_policy
    )

    print(response)


def remove_policy_user(iam_client, user_name, arn_policy):
    """
    Quita una policy a un usuario
    :param iam_client:
    :param user_name:
    :param arn_policy:
    :return:
    """
    response = iam_client.detach_user_policy(
        UserName=user_name,
        PolicyArn=arn_policy
    )

    print(response)


def invoke_lambda(lambda_client, _lambda, data):
    """
    Invoca una lambda pasandole datos
    :param lambda_client:
    :param _lambda:
    :param data: dictionary
    :return:
    """
    response = lambda_client.invoke(
        FunctionName=_lambda,
        Payload=data,
        InvocationType='Event',
    )

    print(response)


def get_lambdas(lambda_client):
    """
    Obtiene el listado de lambdas
    :param lambda_client:
    :return:
    """
    _list_lambdas = lambda_client.get_paginator('list_functions').paginate()

    for _lambdas in _list_lambdas:
        for l in _lambdas['Functions']:
            print(l['FunctionName'])


def create_bucket(s3_client):
    """
    Crea un bucket
    :param s3_client:
    :return:
    """
    response = s3_client.create_bucket(
        Bucket='opensouthtest',
        CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-1',
        },
    )
    print(response)


def upload_file(s3_client, file, bucket):
    """
    Sube un fichero al bucket
    :param s3_client:
    :param file:
    :param bucket:
    :return:
    """
    s3_client.upload_file(file, bucket, file)


def delete_file(s3_client, file, bucket):
    """
    Borra un fichero del bucket
    :param s3_client:
    :param file:
    :param bucket:
    :return:
    """
    print(bucket + file)
    s3_client.delete_object(Bucket=bucket, Key=file)


def download_file(s3_client, file, bucket):
    """
    Descarga un fichero en la carpeta temporal del sistema
    :param s3_client:
    :param file:
    :param bucket:
    :return:
    """
    with open('/tmp/' + file, 'wb') as data:
        s3_client.download_fileobj(bucket, file, data)


def get_files(s3_client, bucket):
    """
    Lista los ficheros de un bucket
    :param s3_client:
    :param bucket:
    :return:
    """

    list_objects = s3_client.list_objects(Bucket=bucket)['Contents']

    for f in list_objects:
        print(f['Key'])


def create_rds(rds_client, rds_data, kms_key_id, monitor_role_arn, db_subnet_group_name, vpc_sg_id,
               ):
    """
    Create a rds
    :param rds_client:
    :param rds_data:
    :param kms_key_id:
    :param monitor_role_arn:
    :param db_subnet_group_name:
    :param vpc_sg_id:
    :return:
    """
    rds_identifier = rds_client.create_db_instance(
        DBName=rds_data['database'],
        DBInstanceIdentifier=rds_data['name'],
        AllocatedStorage=rds_data['volume'],
        DBInstanceClass=rds_data['type'],
        Engine=rds_data['engine'],
        EngineVersion=rds_data['engine_version'],
        MasterUsername=rds_data['user_name'],
        MasterUserPassword=rds_data['pw'],
        VpcSecurityGroupIds=[vpc_sg_id],
        DBSubnetGroupName=db_subnet_group_name,
        DBParameterGroupName=rds_data['db_parameter_group_name'],
        KmsKeyId=kms_key_id,
        BackupRetentionPeriod=7,
        MultiAZ=False,
        AutoMinorVersionUpgrade=True,
        LicenseModel=rds_data['license'],
        PubliclyAccessible=False,
        CopyTagsToSnapshot=True,
        MonitoringRoleArn=monitor_role_arn,
        EnableIAMDatabaseAuthentication=False,
        EnablePerformanceInsights=True,
        PerformanceInsightsKMSKeyId=kms_key_id,
        StorageType='gp2',
        StorageEncrypted=True,
        PerformanceInsightsRetentionPeriod=7,
        MonitoringInterval=1,
    )['DBInstance']['DBInstanceIdentifier']

    print(rds_identifier)
