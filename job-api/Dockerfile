FROM python:3.8.1

WORKDIR /usr/src/app

COPY . .

RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["bash", "-c", "python3 /usr/src/app/run.py"]