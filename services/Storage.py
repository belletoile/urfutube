import boto3
from loguru import logger


class Storage:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',
                               endpoint_url='https://storage.yandexcloud.net',
                               region_name='ru-central1',
                               aws_access_key_id='YCAJEsiRT6SE2LoMX6eIolAgl',
                               aws_secret_access_key='YCMvBDu2XAuo3pJqyMbeL9z53_Y1rXozaAUk1cb5'
                               )

    def save_file(self, file_name):
        try:
            self.s3.upload_file('tmp_files/' + file_name, self.bucket_name, file_name)
        except Exception as e:
            logger.error(f'Возникла ошибка в сохранении файла {e}')
            raise e

        file_url = f'{self.s3.meta.endpoint_url}/{self.bucket_name}/{file_name}'

        return file_url
