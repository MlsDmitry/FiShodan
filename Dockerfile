FROM python:3.9

# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt

#COPY app.py /app.py
ADD . /fish_shodan
WORKDIR /fish_shodan

ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0