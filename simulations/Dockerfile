FROM python:3-slim

COPY requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libxft-dev \
    wget \
    vim \
    libsm6 \
    libxext6 \
    libxrender-dev &&\
    wget https://github.com/opensourcedesign/fonts/raw/master/gnu-freefont_freesans/FreeSansBold.ttf &&\
    mv FreeSansBold.ttf /usr/share/fonts/truetype &&\
    rm -rf /var/lib/apt/lists/* &&\
    pip3 install --upgrade pip &&\
    pip3 install -r /requirements.txt

WORKDIR /app

CMD ["bash","call_defect.sh"]
