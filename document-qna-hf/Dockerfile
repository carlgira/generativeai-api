FROM nvidia/cuda:11.4.3-cudnn8-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install build-essential software-properties-common -y
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install --no-install-recommends -y python3.11 python3.11-venv python3.11-distutils wget
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Dependencies
COPY requirements.txt ./
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.11 get-pip.py
RUN pip3.11 install --upgrade pip
RUN pip3.11 install -r requirements.txt

# App
COPY app.py ./
COPY hf_langchain.py ./
RUN mkdir docs

ARG HUGGINGFACEHUB_API_TOKEN=''
ARG OPENSEARCH_URL=''
ARG HUGGINGFACEHUB_MODEL="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
ARG DOC_CHUNK_SIZE=500
ARG DOC_CHUNK_OVERLAP=100
ARG DOC_MAX_NEW_TOKENS=200
ARG LLM_MAX_NUM_TOKENS=2048

ENV HUGGINGFACEHUB_API_TOKEN=$HUGGINGFACEHUB_API_TOKEN
ENV OPENSEARCH_URL=$OPENSEARCH_URL
ENV HUGGINGFACEHUB_MODEL=$HUGGINGFACEHUB_MODEL
ENV DOC_CHUNK_SIZE=$DOC_CHUNK_SIZE
ENV DOC_CHUNK_OVERLAP=$DOC_CHUNK_OVERLAP
ENV DOC_MAX_NEW_TOKENS=$DOC_MAX_NEW_TOKENS
ENV LLM_MAX_NUM_TOKENS=$LLM_MAX_NUM_TOKENS

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.4"

EXPOSE 3000

CMD ["python3.11", "app.py"]