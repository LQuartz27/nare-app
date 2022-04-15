FROM python:3.9.6
LABEL project="NARE" 
LABEL mantainer="Andres Leal"
ENV FLASK_APP="app.py"
ENV FLASK_DEBUG=1
ENV FLASK_ENV="development"
WORKDIR /nare-app/
COPY . .
RUN apt-get update \
    && apt-get -y install unixodbc unixodbc-dev
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt && rm -rf /root/.cache
CMD flask run --host=0.0.0.0 --port=80