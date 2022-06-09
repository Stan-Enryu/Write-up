FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash ret2

WORKDIR /home/ret2

COPY ./flag.txt .
COPY ./soal .
COPY ./ynetd /usr/bin/ynetd
COPY ./libc-2.31.so .
COPY ./ld.so .

RUN chown -R root:ret2 /home/ret2 && chown root:ret2 /usr/bin/ynetd && chmod -R 750 /home/ret2
RUN chmod 640 flag.txt && chmod 650 /usr/bin/ynetd

USER ret2

EXPOSE 13302
CMD ["/usr/bin/ynetd", "-p", "13302", "/home/ret2/soal"]
