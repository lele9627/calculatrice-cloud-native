FROM debian:latest

RUN apt-get update \
  && apt-get install -y bash htop vim net-tools \
  && rm -rf /var/lib/apt/lists/*

ENV OWNER="leopold"

CMD ["sleep", "3600"]
