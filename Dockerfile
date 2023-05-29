FROM python:3.10.9
# setup environment variable
ENV DockerHOME=/home/app/shopCMS

# set work directory
RUN mkdir -p $DockerHOME


# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY . $DockerHOME
# run this command to install all dependencies
RUN pip install -r requirements.txt

# port where the Django app runs
EXPOSE 8000
ENV PGSSLCERT $DockerHOME/postgresql.crt
python manage.py makemigrations
# start server
CMD gunicorn ShopBackend.wsgi --user www-data --bind 0.0.0.0:8000 --workers 3