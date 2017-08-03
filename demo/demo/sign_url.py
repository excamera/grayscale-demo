import logging
import subprocess
import boto3
import xmltodict
import simplejson as json
import re
from optparse import OptionParser
import sys

def get_signed_url(expires_in, bucket, obj):
      """
      Generate a signed URL
      :param expires_in:  URL Expiration time in seconds
      :param bucket:
      :param obj:         S3 Key name
      :return:            Signed URL
      """
      s3_cli = boto3.client("s3")
      presigned_url = s3_cli.generate_presigned_url('get_object',
                                                  Params = {'Bucket': bucket,
                                                            'Key': obj},
                                                  ExpiresIn = expires_in)
      return presigned_url

(bucket, key) = (sys.argv[1], sys.argv[2])
print (get_signed_url(3000, bucket, key))
