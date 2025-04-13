FROM python:3.8.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 5005 5000

# تشغيل Rasa و Flask معًا
CMD ["bash", "-c", "rasa run --enable-api --cors '*' --debug & python app/main.py"]
