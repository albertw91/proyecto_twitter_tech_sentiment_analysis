FROM python:3.9-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /dash_app
COPY . /dash_app
WORKDIR /dash_app

CMD gunicorn -b 0.0.0.0:8050 app.app:server