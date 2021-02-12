FROM arm64v8/python:3.7-alpine
WORKDIR /app
COPY *.py ./
ENV PYTHONWARNINGS='ignore:Unverified HTTPS request'

RUN pip install requests

CMD ["python3" "./get_unifi_reservations.py"]
