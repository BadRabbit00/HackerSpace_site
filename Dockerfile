# Pull official base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (including fonts for PDF generation and gettext for i18n)
RUN apt-get update && apt-get install -y \
    fonts-dejavu \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Copy entrypoint
COPY ./entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

# Run entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
