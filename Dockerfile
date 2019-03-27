FROM python:2.7
WORKDIR /cloud
COPY . /cloud
RUN pip install -U -r requirements.txt
EXPOSE 8080
CMD ["python", "main.py"]