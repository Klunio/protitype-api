FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt --default-timeout=1000

COPY app app
WORKDIR app

ENV TZ America/New_York

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]