import boto3
import json
import os
import logging
from datetime import datetime

def get_highwatermark(targetbucketname,prefix,init_DateRangeEnd):
    s3 = boto3.client('s3')


    paginator = s3.get_paginator('list_objects_v2')
    #operation_parameters = {'Bucket': targetbucketname,'Prefix': prefix}
    pages = paginator.paginate( Bucket = targetbucketname, Prefix = prefix)
    DateRangeEnd_List = [init_DateRangeEnd]
    for page in pages:
        if 'Contents' in page.keys():
            for obj in page['Contents']:
                print(obj)
                tag = s3.get_object_tagging(
                    Bucket = targetbucketname,
                    Key = obj['Key']
                )
                DateRangeEnd_List.append(tag['TagSet'][0]['Value'])
    return(max(DateRangeEnd_List))            