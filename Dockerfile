FROM python:3.11-alpine

WORKDIR /code

COPY ./req.txt /code/req.txt

RUN pip install --no-cache-dir --upgrade -r /code/req.txt

COPY . /code

RUN mkdir -p /code/tmp_files

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
