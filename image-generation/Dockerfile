FROM nvidia/cuda:11.4.3-cudnn8-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install build-essential software-properties-common -y
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install --no-install-recommends -y python3.11 python3-pip python3-setuptools python3-distutils
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Dependencies
COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# App
COPY app.py ./

ARG HUGGINGFACEHUB_MODEL="stabilityai/stable-diffusion-2-1-base"

ENV HUGGINGFACEHUB_MODEL=$HUGGINGFACEHUB_MODEL

EXPOSE 3000

CMD ["python3.11", "app.py"]