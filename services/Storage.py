import boto3
from loguru import logger

from config import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID


class Storage:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',
                               endpoint_url='https://s3.timeweb.com',
                               region_name='ru-1',
                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                               )

    def save_file(self, file_name):
        try:
            self.s3.upload_file('tmp_files/' + file_name, self.bucket_name, file_name)
        except Exception as e:
            logger.error(f'Возникла ошибка в сохранении файла {e}')
            raise e

        file_url = f'{self.s3.meta.endpoint_url}/{self.bucket_name}/{file_name}'

        return file_url
