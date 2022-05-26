FROM python:3.9.5-buster

WORKDIR /Megatron
RUN chmod 777 /Megatron
RUN apt-get update -y
RUN pip3 install -U pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt
COPY . .
ENV PORT = 8000
EXPOSE 8000
CMD python3 -m Megatron
