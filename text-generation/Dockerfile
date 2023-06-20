FROM nvidia/cuda:11.4.3-cudnn8-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install build-essential software-properties-common -y
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install --no-install-recommends -y python3.11 python3.11-venv python3.11-distutils wget git ffmpeg
RUN apt install --no-install-recommends -y gcc libc-dev libffi-dev g++ make
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Dependencies
COPY requirements.txt ./
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.11 get-pip.py
RUN pip3.11 install --upgrade pip
RUN pip3.11 install -r requirements.txt

# App
COPY app.py ./

ARG HUGGINGFACEHUB_MODEL="bigscience/bloomz-7b1"

ENV HUGGINGFACEHUB_MODEL=$HUGGINGFACEHUB_MODEL

EXPOSE 3000

CMD ["python3.11", "app.py"]