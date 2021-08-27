FROM python:3.8.2
ENV DEBIAN_FRONTEND="noninteractive"
ENV PATH_PWD=/code
ENV PYTHONPATH=.
WORKDIR /code

COPY app/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]