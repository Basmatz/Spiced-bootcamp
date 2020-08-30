# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /twitter_files
WORKDIR /twitter_files

# Copy the requirements file into the container at /twitter_app
# (a text files with all the libraries you want to install)


# Install any needed packages specified in requirements.txt

COPY requirements.txt /twitter_files

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ADD . /twitter_files

# Run get_tweets.py when the container launches
CMD ["python", "get_tweets.py"]
