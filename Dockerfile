# Use Python 3.11 image as base
FROM python:3.11

# Set working directory
WORKDIR /code

# Copy the rest of your application
COPY . /code/
# COPY .env /code/.env

# # Copy requirements first to leverage Docker cache
# COPY ./pyproject.toml /code/pyproject.toml

# Install required packages
RUN pip install --no-cache-dir .


# Expose the port your app runs on
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "start && load_data"]
