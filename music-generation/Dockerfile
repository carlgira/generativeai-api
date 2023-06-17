FROM python:3.9-alpine

RUN apk update && apk add python3-dev gcc libc-dev libffi-dev g++ make rust cargo ffmpeg

# Copy files
COPY app.py ./
COPY requirements.txt ./

# Dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]