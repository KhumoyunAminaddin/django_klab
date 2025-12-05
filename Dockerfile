FROM python:3.13

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8080

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=djangoday.settings

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "makemigrations", "snippets"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
