FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY notes.py .
ENV DB_PATH=/data/notes.db
VOLUME /data
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "notes:app"]