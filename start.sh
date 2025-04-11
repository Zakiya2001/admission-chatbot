#!/bin/bash

# شغّل Rasa في الخلفية
rasa run --enable-api --cors "*" --port 5005 &

# شغّل Flask
python app.py
