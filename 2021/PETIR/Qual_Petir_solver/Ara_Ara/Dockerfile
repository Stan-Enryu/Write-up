FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash ara

WORKDIR /home/ara

COPY ./flag.txt .
COPY ./soal .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:ara /home/ara && chown root:ara /usr/bin/ynetd && chmod -R 750 /home/ara
RUN chmod 640 flag.txt && chmod 650 /usr/bin/ynetd

USER ara

EXPOSE 13304
CMD ["/usr/bin/ynetd", "-p", "13304", "/home/ara/soal"]