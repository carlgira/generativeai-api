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

# App
COPY app.py ./
COPY cohere_langchain.py ./

ARG OPENSEARCH_URL=''
ARG DOC_CHUNK_SIZE=500
ARG DOC_CHUNK_OVERLAP=100
ARG DOC_MAX_NEW_TOKENS=200
ARG LLM_MAX_NUM_TOKENS=4096
ARG COHERE_API_KEY=''
ARG COHERE_MODEL_NAME='command'
ARG COHERE_EMBEDDINGS_MODEL_NAME='multilingual-22-12'

ENV OPENSEARCH_URL=$OPENSEARCH_URL
ENV DOC_CHUNK_SIZE=$DOC_CHUNK_SIZE
ENV DOC_CHUNK_OVERLAP=$DOC_CHUNK_OVERLAP
ENV DOC_MAX_NEW_TOKENS=$DOC_MAX_NEW_TOKENS
ENV LLM_MAX_NUM_TOKENS=$LLM_MAX_NUM_TOKENS
ENV COHERE_API_KEY=$COHERE_API_KEY
ENV COHERE_MODEL_NAME=$COHERE_MODEL_NAME
ENV COHERE_EMBEDDINGS_MODEL_NAME=$COHERE_EMBEDDINGS_MODEL_NAME

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.4"

EXPOSE 3000

CMD ["python3.11", "app.py"]