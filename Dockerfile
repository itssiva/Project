FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/Project/Helloworld
ADD Helloworld/requirements.txt /usr/src/Project/Helloworld
WORKDIR /usr/src/Project/Helloworld/
RUN pip install -r requirements.txt
EXPOSE 11000
