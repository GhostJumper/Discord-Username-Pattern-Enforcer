FROM python:3.9-alpine as base

ARG WORKDIR=/app/

WORKDIR ${WORKDIR}

COPY src/requirements.txt ${WORKDIR}

RUN pip install --no-cache-dir -r requirements.txt

FROM base as final

COPY src/app.py ${WORKDIR}

CMD ["python", "app.py"]
