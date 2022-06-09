FROM ubuntu:16.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash can2

WORKDIR /home/can2

COPY ./flag.txt .
COPY ./soal .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:can2 /home/can2 && chown root:can2 /usr/bin/ynetd && chmod -R 750 /home/can2
RUN chmod 640 flag.txt && chmod 650 /usr/bin/ynetd

USER can2

EXPOSE 13301
CMD ["/usr/bin/ynetd", "-p", "13301", "/home/can2/soal"]