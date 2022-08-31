FROM python:3.9

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ ./

RUN apt update && apt upgrade -y

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
