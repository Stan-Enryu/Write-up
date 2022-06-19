FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd cron && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m filestream && mkdir -p /home/filestream

RUN chown -R root:filestream /home/filestream && chmod 750 /home/filestream

COPY ./flag.txt /home/filestream/flag.txt
COPY ./filestream /home/filestream/filestream
COPY ./xinetd /etc/xinetd.d/xinetd
COPY ./startchall.sh /usr/bin/startchall
COPY ./crontab /etc/crontab

WORKDIR /home/filestream
RUN chown root:filestream flag.txt filestream && chmod 640 flag.txt && chmod 750 filestream && chmod 600 /etc/xinetd.d/xinetd && chmod 755 /usr/bin/startchall && chmod 644 /etc/crontab 

CMD ["/usr/bin/startchall"]
