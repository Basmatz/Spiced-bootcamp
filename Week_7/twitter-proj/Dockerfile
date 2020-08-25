# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /twitter-proj
WORKDIR /Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_7/twitter-proj

# Copy the requirements file into the container at /app
# (a text files with all the libraries you want to install)
ADD requirements.txt /twitter-proj

ADD navalny-tweet.py /twitter-proj

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run navalny-tweet.py when the container launches
CMD ["python", "navalny-tweet.py"]
