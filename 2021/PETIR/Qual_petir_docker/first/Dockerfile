FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash first

WORKDIR /home/first

COPY ./flag.txt .
COPY ./soal .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:first /home/first && chown root:first /usr/bin/ynetd && chmod -R 750 /home/first
RUN chmod 640 flag.txt && chmod 650 /usr/bin/ynetd

USER first

EXPOSE 11101
CMD ["/usr/bin/ynetd", "-p", "11101", "/home/first/soal"]