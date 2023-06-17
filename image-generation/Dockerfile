FROM python:3.9-slim

# Copy files
COPY app.py ./
COPY requirements.txt ./

# Dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]