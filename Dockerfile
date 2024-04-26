FROM python:3.8.6
WORKDIR /blog-platform

COPY . /blog-platform
RUN cd /blog-platform
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install -r requirements.txt

ENV PORT=8000

EXPOSE 8000
CMD [ "sh", "-c", "python3 manage.py runserver 0.0.0.0:8000 --noreload" ]
