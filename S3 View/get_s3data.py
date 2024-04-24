import os
import boto3
from fastapi import FastAPI, HTTPException
from mangum import Mangum

s3 = boto3.resource('s3')
app = FastAPI()
handler = Mangum(app)


s3_client = boto3.client('s3', aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), 
                        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

@app.get("/view_bydate/{device}")
def get_data(device: str):

    try:
        bucket = 'hkt-adc-project'
        prefix = f'{device}/1_originFile/DTG/'

        paginator = s3_client.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate(
            Bucket=bucket,
            Prefix=prefix
        )

        filepaths = []
        for page in response_iterator:
            for content in page['Contents']:
                filepaths.append(content['Key'])

        return {"filepaths": filepaths}
    
    except:
        raise HTTPException(status_code=404, detail="Data not found or invalid device")