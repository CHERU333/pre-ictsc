FROM ubuntu:22.04
RUN apt-get update && apt-get install -y iproute2 iputils-ping python3 ca-certificates
RUN useradd -m user
USER user
WORKDIR /home/user
COPY client.py /home/user/client.py
CMD ["bash","-lc","sleep infinity"]
