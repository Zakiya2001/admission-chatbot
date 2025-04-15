
FROM rasa/rasa:3.1.0

WORKDIR /app

COPY . /app

USER root
RUN chmod +x start.sh

CMD ["./start.sh"]
