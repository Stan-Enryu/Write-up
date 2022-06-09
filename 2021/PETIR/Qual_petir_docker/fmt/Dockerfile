FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash fmt1

WORKDIR /home/fmt1

COPY ./flag.txt .
COPY ./soal .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:fmt1 /home/fmt1 && chown root:fmt1 /usr/bin/ynetd && chmod -R 750 /home/fmt1
RUN chmod 640 flag.txt && chmod 650 /usr/bin/ynetd

USER fmt1

EXPOSE 11104
CMD ["/usr/bin/ynetd", "-p", "11104", "/home/fmt1/soal"]