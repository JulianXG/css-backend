FROM python:2.7

COPY requirements.txt /

ENV TIME_ZONE Asia/Shanghai

RUN echo "${TIME_ZONE}" > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    pip install -r /requirements.txt && rm /requirements.txt

VOLUME /code

EXPOSE 5000

ENTRYPOINT ["python", "/code/app.py"]
