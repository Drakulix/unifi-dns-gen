FROM arm64v8/python:3.7-alpine
WORKDIR /app
COPY *.py ./
COPY run.sh ./
ENV PYTHONWARNINGS='ignore:Unverified HTTPS request'

RUN pip install requests
VOLUME /hosts

CMD ["./run.sh"]
