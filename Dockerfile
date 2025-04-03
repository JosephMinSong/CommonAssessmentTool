# Use Python 3.11 image as base
FROM python:3.11

# Set working directory
WORKDIR /code

# Copy TOML file 
COPY ./pyproject.toml ./pyproject.toml

# Copy startup bash script
COPY ./startup.sh ./startup.sh

# Make sure that we have access to the bash script
RUN chmod +x ./startup.sh

# Copy the rest of your application
COPY ./app /code/app

# Expose the port your app runs on
EXPOSE 8000

# Command to run the application
CMD ["bash", "./startup.sh"]