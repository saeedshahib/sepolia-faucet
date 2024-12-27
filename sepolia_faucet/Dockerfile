FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app/

#RUN python manage.py makemigrations
#RUN python manage.py migrate
# Command to run the application
CMD ["gunicorn", "sepolia_faucet.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
