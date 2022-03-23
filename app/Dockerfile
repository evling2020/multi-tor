FROM alpine

#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk add --no-cache ca-certificates tzdata python3 py3-pip curl wget bash tor gzip && \
    rm -rf /tmp/* && rm -rf /var/cache/apk/*
RUN pip3 install pyyaml==5.4.1
RUN wget -O /tmp/in_program.gz https://github.com/Dreamacro/clash/releases/download/v1.10.0/clash-linux-amd64-v1.10.0.gz && gzip -d /tmp/in_program.gz && mv /tmp/in_program /usr/bin/in_program && chmod +x /usr/bin/in_program
VOLUME /data
COPY entrypoint.sh /entrypoint.sh
COPY init.py /init.py
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
