import asyncio
import io

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from configs import get_configs
from schemas import YandexS3StorageOptionsSchema, S3SBucketKeySchema


class S3Storage:
    def __init__(self, bucket: str = get_configs().bucket_name):
        self.__bucket = bucket
        self.__session = boto3.session.Session()
        self.__s3: BaseClient = self.__session.client(**YandexS3StorageOptionsSchema().dict())
        self.__params: dict | None = None

    async def generate_url(self, filename: str):
        return await asyncio.to_thread(self.__s3.generate_presigned_url, ClientMethod='get_object',
                                       Params=self.__prepare_bucket_and_key(filename=filename),
                                       ExpiresIn=get_configs().expires_in_boto3,
                                       HttpMethod='GET')

    def __prepare_bucket_and_key(self, filename: str) -> dict:
        return S3SBucketKeySchema(Bucket=self.__bucket, Key=f'{filename}').dict(by_alias=True)

    async def save_document(self, filename: str, document: bytes):
        await asyncio.to_thread(self.__s3.upload_fileobj, io.BytesIO(document), self.__bucket, f'specs/{filename}.txt')

    async def is_file_exist(self, filename: str) -> bool:
        try:
            _ = await asyncio.to_thread(self.__s3.head_object, Bucket=self.__bucket, Key=f'specs/{filename}.txt')
            return True
        except ClientError:
            return False
