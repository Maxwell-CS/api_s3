import base64
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    directorio = event['body']['directorio'].strip('/')
    nombre_archivo = event['body']['archivo']
    contenido_b64 = event['body']['contenido_base64']

    # Proceso: el archivo llega codificado en base64
    try:
        contenido = base64.b64decode(contenido_b64)
    except Exception:
        return {'statusCode': 400, 'mensaje': 'contenido_base64 invalido'}

    key = directorio + '/' + nombre_archivo if directorio else nombre_archivo
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=nombre_bucket, Key=key, Body=contenido)
    except ClientError as e:
        return {
            'statusCode': 400,
            'error': e.response['Error']['Code'],
            'mensaje': e.response['Error']['Message']
        }

    # Salida
    return {
        'statusCode': 200,
        'mensaje': 'Archivo subido',
        'bucket': nombre_bucket,
        'key': key,
        'bytes': len(contenido)
    }
