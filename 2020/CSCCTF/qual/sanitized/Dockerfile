FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m sanitized && mkdir -p /home/sanitized

RUN chown -R root:sanitized /home/sanitized && chmod 750 /home/sanitized

COPY ./flag.txt /home/sanitized/flag.txt
COPY ./sanitized /home/sanitized/sanitized
COPY ./xinetd /etc/xinetd.d/xinetd
COPY ./startchall.sh /usr/bin/startchall

WORKDIR /home/sanitized
RUN chown root:sanitized flag.txt sanitized && chmod 640 flag.txt && chmod 750 sanitized && chmod 600 /etc/xinetd.d/xinetd && chmod 755 /usr/bin/startchall

CMD ["/usr/bin/startchall"]
