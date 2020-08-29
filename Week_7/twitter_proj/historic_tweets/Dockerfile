# Dockerfile for historic_tweets

# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Name the working directory within the container to /app # /app exists only in the container
WORKDIR /app

# Copy the requirements file into the container at /app
# (a text files with all the libraries you want to install)
ADD credentials.py /app

ADD requirements_historic.txt /app

ADD older_navalny_tweets.py /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements_historic.txt

# Run navalny_tweet_to_db.py when the container launches
CMD ["python", "older_navalny_tweets.py"]
