#!/bin/bash

# Start Rasa in background
rasa run --enable-api --cors "*" --debug --port 5005 &

# Wait a bit to make sure Rasa starts properly
sleep 5

# Start Flask app (assuming it's app.py)
python3 app.py
