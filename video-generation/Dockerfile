
FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg git

# Copy files
COPY app.py ./
COPY requirements.txt ./

RUN git clone -b dev https://github.com/camenduru/Text-To-Video-Finetuning
RUN git clone https://huggingface.co/camenduru/potat1

# Dependencies
RUN pip3 install --upgrade pip
RUN pip3 install torch
RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]





