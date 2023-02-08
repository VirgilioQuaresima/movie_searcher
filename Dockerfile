FROM python:3.9-alpine3.16

WORKDIR /app

COPY ./src .

COPY requirements.txt /app

EXPOSE 5000

RUN pip3.9 install --no-cache-dir --upgrade -r requirements.txt

CMD ["flask", "--app", "server.py" ,"run" ,"--host","0.0.0.0"]

