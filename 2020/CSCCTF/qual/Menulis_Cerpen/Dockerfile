FROM ubuntu:20.04

RUN apt-get update && apt-get install -y socat && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

RUN useradd -U -m cerpen && mkdir -p /home/cerpen

RUN chown -R root:cerpen /home/cerpen && chmod 750 /home/cerpen

COPY ./flag.txt /home/cerpen/flag.txt
COPY ./cerpen /home/cerpen/cerpen
COPY ./libc.so.6 /home/cerpen/libc.so.6
COPY ./ld.so /home/cerpen/ld.so

WORKDIR /home/cerpen
RUN chown root:cerpen flag.txt cerpen ld.so libc.so.6 && chmod 640 flag.txt && chmod 750 cerpen libc.so.6 ld.so

CMD ["socat","TCP4-LISTEN:13339,reuseaddr,fork,su=cerpen","EXEC:'./cerpen'"]
