FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /history
COPY requirements.txt /history/
RUN pip install -r requirements.txt
COPY . .