FROM ubuntu:19.04

RUN useradd --create-home --shell /bin/bash ctf



WORKDIR /home/ctf

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf

COPY ./share/<REDACTED FLAG> /

CMD ["xinetd", "-dontfork"]
