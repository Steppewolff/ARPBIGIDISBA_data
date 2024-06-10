# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# setup environment variable
ENV DockerHOME=/home/frontend

# Set the working directory
RUN mkdir -p $DockerHOME
WORKDIR /home/frontend

# update pip
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY . $DockerHOME

# Install dependencies
RUN pip install -r requirements.txt

# Exposing interface port
EXPOSE 8000

## Configurando migraciones
#CMD ["python3", "./ARPBIGIDISBA_frontend/manage.py", "makemigrations"]

# Migrating models changes
CMD ["python3", "./ARPBIGIDISBA_frontend/manage.py", "migrate"]

# Starting Django app
CMD ["python3", "./ARPBIGIDISBA_frontend/manage.py", "runserver", "0.0.0.0:8000"]
