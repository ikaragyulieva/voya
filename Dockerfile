FROM python:3.12

# Install system packages needed by WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0  \
    libpangocairo-1.0-0  \
    libcairo2 libffi-dev  \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for the Django project (Voya project)
WORKDIR /voya

# Copy the requirements.txt file and installing the dependencies
COPY requirements.txt /voya/
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn (when in Production)
RUN pip install gunicorn gevent  # gevent included as asynchronous workers will be used

# Copy the rest of the project code into the container
COPY . /voya/

# **Copy the run_gunicorn.py to the container root**
COPY run_gunicorn.py /run_gunicorn.py
RUN chmod +x /run_gunicorn.py

# Copy a custom entrypoint script that will:
# 1) run migrations
# 2) collect static
# 3) start Gunicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port voya app is running on (using default Django port)
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
