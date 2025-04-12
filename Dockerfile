FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 5005 5000

# تشغيل Rasa و Flask معًا
CMD rasa run --enable-api --cors "*" --debug &
CMD python app/main.py
