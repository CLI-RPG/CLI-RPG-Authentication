FROM python:3.10
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY auth_server.py /app/auth_server.py
WORKDIR /app
EXPOSE 5000
CMD ["python", "auth_server.py"]