FROM ubuntu:latest

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m immovable && mkdir -p /home/immovable

RUN chown -R root:immovable /home/immovable && chmod 750 /home/immovable

COPY ./flag.txt /home/immovable/flag.txt
COPY ./immovable /home/immovable/immovable
COPY ./xinetd /etc/xinetd.d/xinetd
COPY ./startchall.sh /usr/bin/startchall

WORKDIR /home/immovable
RUN chmod 640 flag.txt && chmod 750 immovable && chmod 600 /etc/xinetd.d/xinetd && chmod 755 /usr/bin/startchall

CMD ["/usr/bin/startchall"]