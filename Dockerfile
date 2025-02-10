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

# Gunicorn config (only when in Production)
#COPY gunicorn.conf.py /voya/gunicorn.conf.py

# Collect static files (only when in Production)
#RUN python manage.py collectstatic --noinput

# Copy a custom entrypoint script that will:
# 1) run migrations
# 2) collect static
# 3) start Gunicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port voya app is running on (using default Django port)
EXPOSE 8000

# Set default command to run the Django dev server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

ENTRYPOINT ["/entrypoint.sh"]

#Set default command to run Gunicorn (when in Production)
#CMD ["gunicorn", "-c", "gunicorn.conf.py", "voya.wsgi:application"]
