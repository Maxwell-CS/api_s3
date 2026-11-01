import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    directorio = event['body']['directorio'].strip('/')

    # Proceso: en S3 un "directorio" es un objeto vacio cuya clave termina en "/"
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=nombre_bucket, Key=directorio + '/')
    except ClientError as e:
        return {
            'statusCode': 400,
            'error': e.response['Error']['Code'],
            'mensaje': e.response['Error']['Message']
        }

    # Salida
    return {
        'statusCode': 200,
        'mensaje': 'Directorio creado',
        'bucket': nombre_bucket,
        'directorio': directorio + '/'
    }
