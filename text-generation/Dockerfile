FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libc-dev libffi-dev g++ make ffmpeg

# Dependencies
COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install torch
RUN pip3 install -r requirements.txt

# App
COPY app.py ./

ARG HUGGINGFACEHUB_MODEL="bigscience/bloomz-7b1"

ENV HUGGINGFACEHUB_MODEL=$HUGGINGFACEHUB_MODEL

EXPOSE 3000

CMD ["python", "app.py"]