FROM python:3.12

WORKDIR /app

COPY /backend/scraper.py /app/backend/scraper.py
COPY /backend/*.json /app/backend/
COPY /frontend/dist/ /app/frontend/dist/
COPY app.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-w", "2", "app:app"]