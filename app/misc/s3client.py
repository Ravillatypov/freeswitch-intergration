import hashlib
from datetime import datetime
from string import hexdigits

import boto3

HEX_DIGITS = hexdigits[:-6]


class S3Client:
    client = None
    endpoint_url = 'https://storage.yandexcloud.net'

    def __init__(self, bucket_name, folder_name):
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name='s3',
            endpoint_url=self.endpoint_url
        )
        self.bucket_name = bucket_name
        self.folder_name = folder_name

    def upload(self, filename: str, content: bytes) -> str:
        """
        Upload a file to S3

        :param str filename: File name
        :param bytes content: File content
        :param str dst_path: Destination path
        :return dict Response:

        :raises RuntimeError In the case if a file wasn't uploaded successfully
        """
        f_hash = hashlib.md5(content).hexdigest()
        dst_path = datetime.today().strftime("%Y/%m/%d")

        resp = self.client.put_object(
            Bucket=self.bucket_name,
            Key=f'{self.folder_name}/{dst_path}/{filename}',
            Body=content,
            ContentLength=len(content),
        )

        info = self.client.head_object(
            Bucket=self.bucket_name,
            Key=f'{self.folder_name}/{dst_path}/{filename}'
        )

        if resp.get('ETag', '') != f'"{f_hash}"' or info.get('ContentLength', 0) == 0:
            raise RuntimeError(f"File \"{filename}\" wasn't uploaded")

        return f'{self.endpoint_url}/{self.bucket_name}/{self.folder_name}/{dst_path}/{filename}'
