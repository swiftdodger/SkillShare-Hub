FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for building wheels (adjust if using a DB like postgres)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

# non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

ENV PORT=8000
EXPOSE 8000

# default command for running the Django app with gunicorn
CMD ["gunicorn", "LearningPlatform.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]