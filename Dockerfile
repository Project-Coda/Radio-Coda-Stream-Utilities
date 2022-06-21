FROM debian:bullseye
ARG S6_OVERLAY_VERSION=3.1.1.0
COPY rootfs /
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3 \
    xz-utils
RUN pip3 install flask
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz
ADD https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz /tmp
RUN tar --strip-components=1 -C /usr/local/bin -Jxpf /tmp/ffmpeg-release-amd64-static.tar.xz

ENTRYPOINT ["/init"]