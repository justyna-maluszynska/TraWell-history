FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /history_rides
COPY requirements.txt /history_rides/
RUN pip install -r requirements.txt
COPY . .