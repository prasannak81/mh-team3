FROM python:3

WORKDIR /usr/local/src

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "mvsensor.py"]
