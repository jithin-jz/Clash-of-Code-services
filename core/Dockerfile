FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -g 10001 appuser \
    && useradd -m -u 10001 -g 10001 appuser

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY --chown=appuser:appuser . .

# Copy static files directly from installed packages — bypasses collectstatic entirely.
# collectstatic returns 0 files due to cloudinary_storage app interference at build time.
RUN mkdir -p /app/staticfiles/admin /app/staticfiles/rest_framework \
    && cp -R $(python -c "import django, os; print(os.path.join(os.path.dirname(django.__file__), 'contrib/admin/static/admin'))")/* /app/staticfiles/admin/ \
    && cp -R $(python -c "import rest_framework, os; print(os.path.join(os.path.dirname(rest_framework.__file__), 'static/rest_framework'))")/* /app/staticfiles/rest_framework/ \
    && chown -R appuser:appuser staticfiles \
    && echo "Static files:" && ls -la /app/staticfiles/


EXPOSE 8000

USER appuser

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
