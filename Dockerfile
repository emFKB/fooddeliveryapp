FROM python:3.8.10

COPY requirement.txt requirement.txt
RUN pip install --no-cache-dir -r requirement.txt

COPY . code
WORKDIR /code

EXPOSE 8080

ENTRYPOINT ["python", "fooddeliveryapp/manage.py"]
CMD ["runserver", "0.0.0.0:8080"]