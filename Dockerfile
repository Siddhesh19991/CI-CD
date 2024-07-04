FROM --platform=linux/amd64 python:3.12.1
WORKDIR /app
ADD . /app 
RUN pip install --trusted-host pypi.python.org -r requirements_doc.txt 
EXPOSE 5000
CMD ["python","app.py"]
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
