FROM ubuntu:latest

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m babysc && mkdir -p /home/babysc

RUN chown -R root:babysc /home/babysc && chmod 750 /home/babysc && mkdir /home/babysc/55ffa688e1003d7020b4b2b0e84b85fc

COPY ./flag.txt /home/babysc/55ffa688e1003d7020b4b2b0e84b85fc/flag.txt
COPY ./babysc /home/babysc/babysc
COPY ./xinetd /etc/xinetd.d/xinetd
COPY ./startchall.sh /usr/bin/startchall


WORKDIR /home/babysc
RUN chown -R root:babysc ./55ffa688e1003d7020b4b2b0e84b85fc babysc && chmod 640 ./55ffa688e1003d7020b4b2b0e84b85fc/flag.txt && chmod 750 ./55ffa688e1003d7020b4b2b0e84b85fc babysc && chmod 600 /etc/xinetd.d/xinetd && chmod 755 /usr/bin/startchall

CMD ["/usr/bin/startchall"]
