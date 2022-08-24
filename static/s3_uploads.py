import boto3
from botocore.config import Config
import os
import json
from django.core.cache import cache


S3_BUCKET = os.environ.get('S3_LOGBOOKS_BUCKET')
AWS_ACCESS_KEY = os.environ.get('ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_DEFAULT_REGION')

print(S3_BUCKET)
print(AWS_ACCESS_KEY)
print(AWS_SECRET_KEY)
print(AWS_REGION)






client_s3 = boto3.client('s3',
                            aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY,
                            config = Config(signature_version='s3v4', max_pool_connections=20))

#create a presigned post url for uploads
def presigned_url(file_name, file_type):
    presigned_post = client_s3.generate_presigned_post(Bucket=S3_BUCKET,
                                                       Key=file_name, 
                                                       Fields = {"Content-Type": file_type},
                                                       Conditions = [{"Content-Type": file_type}],
                                                       ExpiresIn = 5000)

    return json.dumps(presigned_post) 



#create a prsigned url for downloads
def get_s3file(file_name, expires = 5000):
    response = client_s3.generate_presigned_url(
        ClientMethod = "get_object",
        ExpiresIn = expires,
        Params = {"Bucket" : S3_BUCKET, "Key" : file_name, "ResponseContentDisposition": 'attachment'})
    return response                     
