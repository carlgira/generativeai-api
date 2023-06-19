FROM python:3.11-slim

RUN apt-get update && apt-get install -y git

# Dependencies
COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# App
COPY app.py ./

EXPOSE 3000

CMD ["python", "app.py"]