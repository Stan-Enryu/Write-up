FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m linkedbin && mkdir -p /home/linkedbin

RUN chown -R root:linkedbin /home/linkedbin && chmod 750 /home/linkedbin

COPY ./flag.txt /home/linkedbin/flag.txt
COPY ./linkedbin /home/linkedbin/linkedbin
COPY ./xinetd /etc/xinetd.d/xinetd
COPY ./startchall.sh /usr/bin/startchall

WORKDIR /home/linkedbin
RUN chown root:linkedbin flag.txt linkedbin && chmod 640 flag.txt && chmod 750 linkedbin && chmod 600 /etc/xinetd.d/xinetd && chmod 755 /usr/bin/startchall

CMD ["/usr/bin/startchall"]