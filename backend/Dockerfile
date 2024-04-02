# Use Python image with tag "3.12-alpine"
FROM python:3.12-alpine

# Set system environments
ENV PYTHONUNBUFFERED 1

# Set docker build argument (define: prod or dev build)
ARG DEV=false

# Copy our requirements files into tmp directory
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Set container workdir directory
WORKDIR /app

# Copy source directory with application into container directory
COPY ./app .


# Create virtual environment into workdir
RUN python -m venv /py && \
    # Upgrade pip
    /py/bin/pip install --upgrade pip && \
    # Install required dependencies for our requirements.txt
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    # Install dependencies from file requirements.txt
    /py/bin/pip install -r /tmp/requirements.txt && \
    # If argument DEV set to "true" then install requirements.dev.txt
    if [ $DEV="true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    # Remove tmp directory with our (already installed) requirements files
    rm -rf /tmp && \
    # Remove unnecessary build dependencies
    apk del .tmp-build-deps && \
    # Create system user
    adduser --disabled-password --no-create-home django-user

# Set user that the Docker container will run
USER django-user

# Set the environment variable PATH to include the directory /py/bin
ENV PATH="/py/bin:$PATH"

# Expose port 8000 for access to server
EXPOSE 8000

# Start Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
