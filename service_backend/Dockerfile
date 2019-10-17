# Use an official Python runtime as a parent image
FROM python:3.7-buster

# Set the working directory to /app
WORKDIR /app

ADD requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000
#CMD ["python", "main.py"]
