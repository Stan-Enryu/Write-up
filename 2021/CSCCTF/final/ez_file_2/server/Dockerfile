FROM ubuntu:latest

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash ezfile2

WORKDIR /home/ezfile2

COPY ./flag.txt .
COPY ./ld-2.29.so .
COPY ./libc-2.29.so .
COPY ./chall .
COPY ./run.sh ./run
COPY ./xinetd /etc/xinetd.d/xinetd
COPY ./startchall.sh /usr/bin/startchall

RUN chown -R root:ezfile2 /home/ezfile2 && chmod -R 550 /home/ezfile2
RUN chmod 440 flag.txt && chmod 500 /etc/xinetd.d/xinetd && chmod 500 /usr/bin/startchall
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

CMD ["/usr/bin/startchall"]
