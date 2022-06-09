FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash fmt2

WORKDIR /home/fmt2

COPY ./flag.txt .
COPY ./soal .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:fmt2 /home/fmt2 && chown root:fmt2 /usr/bin/ynetd && chmod -R 750 /home/fmt2
RUN chmod 640 flag.txt && chmod 650 /usr/bin/ynetd

USER fmt2

EXPOSE 13303
CMD ["/usr/bin/ynetd", "-p", "13303", "/home/fmt2/soal"]