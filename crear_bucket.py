import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']

    # Proceso
    s3 = boto3.client('s3')
    try:
        # us-east-1 NO admite LocationConstraint
        s3.create_bucket(Bucket=nombre_bucket)
    except ClientError as e:
        return {
            'statusCode': 400,
            'error': e.response['Error']['Code'],
            'mensaje': e.response['Error']['Message']
        }

    # Salida
    return {
        'statusCode': 200,
        'mensaje': 'Bucket creado',
        'bucket': nombre_bucket
    }
