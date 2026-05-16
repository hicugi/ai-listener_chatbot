FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

WORKDIR /app
RUN mkdir records
COPY ./requirements.txt .

RUN apt-get update && apt-get install -y \
    wget \
    ffmpeg \
    pulseaudio \
    portaudio19-dev \
    cmake \
    pkg-config \
    python3.10 \
    python3.10-distutils \
    python3-pip \
    python3-venv \
    portaudio19-dev python3-pyaudio

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade pip setuptools wheel

CMD ["bash"]
