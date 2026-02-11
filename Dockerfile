FROM ubuntu

EXPOSE 80

COPY app.py .
COPY requirements.txt .
COPY images/* images/
COPY README.md .

RUN apt-get update
RUN apt-get install python3 python3-pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
