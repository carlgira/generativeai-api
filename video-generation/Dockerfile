FROM nvidia/cuda:11.4.3-cudnn8-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install build-essential software-properties-common -y
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install --no-install-recommends -y python3.11 python3.11-venv python3.11-dev python3.11-distutils wget git git-lfs ffmpeg
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Dependencies
COPY requirements.txt ./
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.11 get-pip.py
RUN pip3.11 install --upgrade pip
RUN pip3.11 install -r requirements.txt

RUN git clone https://github.com/ExponentialML/Text-To-Video-Finetuning  && cd Text-To-Video-Finetuning && git checkout 89221af707bf57dfba6fc5918c2f62d0886d4aa8 && cd ..
RUN git clone https://huggingface.co/camenduru/potat1 && cd potat1 && git checkout 0025067347b65c89c56353259c41912b5de6fe7e && cd ..

# App
COPY app.py ./

EXPOSE 3000

CMD ["python3.11", "-u", "app.py"]





