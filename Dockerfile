FROM python:3.10.12
RUN python -m pip install --upgrade pip
RUN pip install poetry

COPY . /app
WORKDIR /app

COPY dp_temp_anomaly_model.h5 /app
COPY pyproject.toml /app
COPY tests /app

RUN poetry config virtualenvs.create false
RUN poetry install

RUN curl -LO http://db.csail.mit.edu/labdata/data.txt.gz
RUN gzip -dv data.txt.gz

EXPOSE 9090
ENTRYPOINT ["python"]
CMD ["app/app.py"]
