FROM python:3.6.10

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . .

CMD ["bash", "-c", "python3 /usr/src/app/run.py"]
