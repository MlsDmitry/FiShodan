FROM python:3.9

# layer caching for faster builds
RUN pip install -r /requirements.txt

#COPY app.py /app.py
WORKDIR /fish_shodan

ENV FLASK_ENV=development

CMD python