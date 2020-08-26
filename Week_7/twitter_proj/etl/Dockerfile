# Dockerfile for ETL

# official Python runtime as parent image
FROM python:3.6-slim

# Name the working directory within the container to /app # /app exists only in the container
WORKDIR /app

# Copy the requirements file into the container at /app
# (a text files with all the libraries you want to install)

ADD requirements_etl.txt /app

ADD navalny_etl.py /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements_etl.txt

# Run navalny_tweet.py when the container launches
CMD ["python", "navalny_etl.py"]
