FROM python:2.7

COPY requirements.txt /

RUN pip install -r /requirements.txt && rm /requirements.txt

VOLUME /code

EXPOSE 5000

ENTRYPOINT ["python", "/code/app.py"]
