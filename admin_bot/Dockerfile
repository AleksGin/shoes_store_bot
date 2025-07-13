FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1\
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /admin_bot

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY admin_bot .

COPY shared ./shared

CMD ["python", "main.py"]