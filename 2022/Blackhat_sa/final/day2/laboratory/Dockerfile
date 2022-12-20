FROM ubuntu:22.04




RUN apt-get update && apt-get -y upgrade
RUN useradd -d /home/task/ -m -p task -s /bin/bash task
RUN echo "task:task" | chpasswd
RUN apt-get install -y binutils gdb
WORKDIR /home/task

COPY ./main .
COPY ./flag.txt .
COPY ./ynetd .
COPY ./run.sh .
RUN chmod 555 /home/task
RUN chmod 555 ./main
RUN chmod 666 ./flag.txt
RUN chmod 555 ./ynetd
RUN chmod 755 ./run.sh

USER task
CMD ./run.sh
