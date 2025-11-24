FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy the source code
COPY src /app/src

# Copy the notebooks
COPY notebooks /app/notebooks

# Copy the environment variables
COPY .env /app/.env

# Expose the necessary port (if applicable)
# EXPOSE 8080

# Command to run the application (modify as needed)
CMD ["python", "-m", "src.sagemaker_entry"]