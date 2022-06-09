FROM ubuntu:16.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash can1

WORKDIR /home/can1

COPY ./flag.txt .
COPY ./soal .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:can1 /home/can1 && chown root:can1 /usr/bin/ynetd && chmod -R 750 /home/can1
RUN chmod 640 flag.txt && chmod 650 /usr/bin/ynetd

USER can1

EXPOSE 11102
CMD ["/usr/bin/ynetd", "-p", "11102", "/home/can1/soal"]