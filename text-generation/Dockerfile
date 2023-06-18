FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libc-dev libffi-dev g++ make ffmpeg

# Copy files
COPY app.py ./
COPY requirements.txt ./

# Dependencies
RUN pip3 install --upgrade pip
RUN pip3 install torch
RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]