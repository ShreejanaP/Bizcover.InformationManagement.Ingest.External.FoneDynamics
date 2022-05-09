import boto3
import json
import os
import logging
from datetime import datetime

def push_to_s3(file_directory,prefix,result_file_name,highwatermark):
    try:
        objectname =  prefix  + result_file_name
        s3 = boto3.client('s3') 
        print(os.environ['targetbucket'])
        print(objectname)
        with open(file_directory + result_file_name, "rb") as f:
            s3.upload_fileobj(f, os.environ['targetbucket'], objectname)

        s3.put_object_tagging(Bucket = os.environ['targetbucket'], 
            Key = objectname,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'DateRangeEnd',
                        'Value': highwatermark
                    },
                ]
            }       
        )



    except Exception as error:
        logging.error('Upload to S3 failed : %s' % error)


