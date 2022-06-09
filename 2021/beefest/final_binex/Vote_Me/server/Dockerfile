FROM ubuntu:latest

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash voteme

WORKDIR /home/voteme

COPY ./flag.txt .
COPY ./chall .
COPY ./run.sh ./run
COPY ./xinetd /etc/xinetd.d/xinetd
COPY ./startchall.sh /usr/bin/startchall

RUN chown -R root:voteme /home/voteme && chmod -R 550 /home/voteme
RUN chmod 440 flag.txt && chmod 500 /etc/xinetd.d/xinetd && chmod 500 /usr/bin/startchall
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

CMD ["/usr/bin/startchall"]
