# Use Python 3.11 image as base
FROM python:3.11

# Set working directory
WORKDIR /code

# Copy TOML file 
COPY ./pyproject.toml /code/pyproject.toml

# Copy startup bash script
COPY ./startup.sh /code/startup.sh

# Make sure that we have access to the bash script
RUN chmod +x /code/startup.sh

# Copy db
COPY ./sql_app.db /code/
COPY ./test.db /code/

# Copy the rest of your application
COPY ./app /code/app

# Expose the port your app runs on
EXPOSE 8000

# Command to run the application
CMD ["bash", "./startup.sh"]