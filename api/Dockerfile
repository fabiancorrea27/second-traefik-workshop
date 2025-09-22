FROM python:3.9-alpine
WORKDIR /app
RUN pip install flask neo4j
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]