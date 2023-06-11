import os

from fastapi import File, UploadFile
from loguru import logger

from services.Storage import Storage


def save_video(file: UploadFile = File(...)):
    try:
        with open('tmp_files/' + file.filename, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)

        s3 = Storage('38cfe289-urfutube')
        file_url = s3.save_file(file.filename)
    except Exception as e:
        logger.error(f'Возникла ошибка в сохранении файла {e}')
        raise e

    finally:
        file.file.close()
        if os.path.isfile('tmp_files/' + file.filename):
            os.remove('tmp_files/' + file.filename)

    return file_url
