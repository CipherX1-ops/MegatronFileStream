FROM python:3.9.2-slim-buster

RUN chmod +x /usr/local/bin/*

RUN git clone https://github.com/CipherX1-ops/MegatronFileStream.git

RUN pip3 install -r requirements.txt

CMD ["bash", "start.sh"]
