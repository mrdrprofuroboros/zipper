FROM python:3.6

WORKDIR /app
COPY ./zopfli /app/zopfli
COPY ./infgen /app/infgen

RUN cd zopfli && make && cd .. &&\
    cd infgen && gcc infgen.c -lm -O2 -o infgen

COPY ./zipper.py /app/zipper.py

CMD ["python", "zipper.py"]