FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash ret1

WORKDIR /home/ret1

COPY ./flag.txt .
COPY ./soal .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:ret1 /home/ret1 && chown root:ret1 /usr/bin/ynetd && chmod -R 750 /home/ret1
RUN chmod 640 flag.txt && chmod 650 /usr/bin/ynetd

USER ret1

EXPOSE 11103
CMD ["/usr/bin/ynetd", "-p", "11103", "/home/ret1/soal"]