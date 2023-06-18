FROM python:3.11-slim

# Copy files
COPY app.py ./
COPY requirements.txt ./

# Dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


ARG HUGGINGFACEHUB_MODEL="stabilityai/stable-diffusion-2-1-base"

ENV HUGGINGFACEHUB_MODEL=$HUGGINGFACEHUB_MODEL

EXPOSE 3000

CMD ["python", "app.py"]