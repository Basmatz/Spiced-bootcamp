# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /tweet_collector
WORKDIR /tweet_collector

# Copy the requirements file into the container at /tweet_collector
# (a text files with all the libraries you want to install)
#ADD requirements.txt /tweet_collector

COPY requirements.txt /tweet_collector


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD . /tweet_collector


# Run get_tweets.py when the container launches
CMD ["python", "get_tweets.py"]