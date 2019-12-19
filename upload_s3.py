import hmac
import uuid

import boto3.session


class GeneratePresignedURL:

    def __init__(self, aws_access_key, aws_secret_key, bucket_region):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        session = boto3.session.Session(region_name=bucket_region)
        self.s3_obj = session.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            config=boto3.session.Config(signature_version='s3v4'))

    def _get_digest(self, msg):
        result = hmac.new(self.aws_access_key.encode('utf-8'),
                          msg=msg.encode('utf-8'))
        return result.hexdigest()

    def generate_presigned_url(self, key, bucket_name, expiry=3600):
        """Generate presigned GET url."""
        return self.s3_obj.generate_presigned_url(
            'get_object', Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=expiry)

    def generate_presigned_post(self, key, bucket_name, expiry=3600):
        """Generate presigned POST url."""
        d = self.s3_obj.generate_presigned_post(
            bucket_name, key, ExpiresIn=expiry)
        d.update({'digest': self._get_digest(key)})
        return d
