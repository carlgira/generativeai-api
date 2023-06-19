FROM python:3.11-slim

# Dependencies
COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# App
COPY app.py ./

ARG HUGGINGFACEHUB_MODEL="stabilityai/stable-diffusion-2-1-base"

ENV HUGGINGFACEHUB_MODEL=$HUGGINGFACEHUB_MODEL

EXPOSE 3000

CMD ["python", "app.py"]