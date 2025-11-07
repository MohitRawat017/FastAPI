# Base Image 
FROM python:3.9-slim
# working directory 
WORKDIR /app
# copy files
COPY . /app
# run commands
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000


# in the terminal run the command
# docker build -t my-python-app .
# docker run -p 8000:5000 my-python-app
# 8000 port on host maps to 5000 in the container 