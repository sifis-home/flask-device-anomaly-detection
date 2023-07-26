FROM python:3.10
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN pip install pillow==9.2.0
RUN pip install websocket-client
RUN pip install rel

COPY . /app
WORKDIR /app

COPY dp_temp_anomaly_model.h5 /app
COPY pyproject.toml /app
COPY tests /app

RUN poetry config virtualenvs.create false
RUN poetry install

RUN curl -LO http://db.csail.mit.edu/labdata/data.txt.gz
RUN gzip -dv data.txt.gz

# RUN pip install -r requirements.txt
EXPOSE 9090
ENTRYPOINT ["python"]
CMD ["app/app.py"]
