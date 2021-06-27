FROM python:3.9.5-buster

WORKDIR /Megatron
RUN chmod 777 /Megatron
RUN apt-get update -y
RUN apt-get install -y wget curl bash git 

#Updating Libraries
RUN pip3 install -U pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

# If u want to use /update feature, uncomment the following and edit
#RUN git config --global user.email "your_email"
#RUN git config --global user.name "git_username"

#Copying All Source
COPY . .

#Starting Bot
CMD ["python3", "-m", "Megatron"]
