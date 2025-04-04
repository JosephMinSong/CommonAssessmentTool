# Use Python 3.11 image as base
FROM python:3.11

# Set working directory
WORKDIR /code

# Copy TOML file 
COPY ./pyproject.toml /code/pyproject.toml

# Run pip install .
RUN pip install .

# Run pip install -e .
RUN pip install -e .

# Copy the rest of your application
COPY ./app /code/app

ENV PYTHONPATH=/code

# Expose the port your app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "app/run.py"]