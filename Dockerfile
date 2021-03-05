FROM python:3.8

WORKDIR /src

ADD ./src /src

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.api.api:app", "--host", "0.0.0.0", "--port", "8000"]
