FROM arm32v7/python:3.7.10-buster

WORKDIR /app

COPY ./blink_LED.py ./

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install rpi.gpio

CMD ["python", "./blink_LED.py"]
