FROM alpine:3.18.4
COPY now-playing.py /now-playing.py
COPY requirements.txt /requirements.txt
RUN apk add --no-cache python3 py3-pip
RUN pip3 install -r requirements.txt
CMD ["python3", "now-playing.py"]