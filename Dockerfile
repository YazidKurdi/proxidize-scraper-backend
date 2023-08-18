# Use the base image
FROM selenium/standalone-chrome


USER root

# Set the working directory
WORKDIR /app

# Copy your Django project files to the container
COPY . /app/

# Install any additional dependencies you need
RUN apt-get update && apt-get install python3-distutils -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Run Django makemigrations and migrate commands
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Expose the port your Django app will run on
EXPOSE 8000

# Command to run your Django server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "core.wsgi:application"]
