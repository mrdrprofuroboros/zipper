FROM python:3.6

WORKDIR /app
COPY . /app

RUN cd zopfli && make && cd .. && \
    cd infgen && gcc infgen.c -lm -O2 -o infgen

CMD ["python", "zipper.py"]
# CMD inf.sh