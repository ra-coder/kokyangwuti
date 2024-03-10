FROM python:3.12

WORKDIR /code

COPY requirements.in .
RUN pip install --no-cache-dir -r requirements.in

COPY src src

WORKDIR /code/src

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]