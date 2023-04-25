FROM python:3.11
COPY requirements.txt requirments.txt
RUN pip3 install -r requirments.txt
COPY . /app
WORKDIR app
CMD ["python3", "start_app.py"]

