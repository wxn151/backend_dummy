# load Python
FROM python:3.11-slim

# workflow PATH
WORKDIR /app

# do a copy
COPY . .

# dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# default port
EXPOSE 8000

# command to DEPLOY
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
