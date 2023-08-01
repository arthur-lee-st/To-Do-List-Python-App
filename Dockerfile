FROM python:3.11.2-alpine

WORKDIR /to_do_app

COPY /to_do_app /to_do_app

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "todoapp.py"]