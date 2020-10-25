
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /car_service

# Set the working directory
WORKDIR /car_service

# Copy the current directory contents into the container
ADD . /car_service/

# Install all packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


