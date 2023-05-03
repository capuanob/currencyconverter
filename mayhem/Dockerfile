# Build Stage
FROM bcapuano/atheris:2.1.1-python3.10
ADD . /src
WORKDIR /src
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y git
RUN python3 -m pip install .

CMD ["/src/mayhem/fuzz_money.py"]
