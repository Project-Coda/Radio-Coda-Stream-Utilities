FROM nvidia/cuda:11.0.3-base-ubuntu20.04
ARG S6_OVERLAY_VERSION=3.1.1.0
COPY rootfs /
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3 \
    xz-utils \
    build-essential \
    yasm \
    cmake \
    libtool \
    libc6 \
    libc6-dev \
    unzip \
    wget \
    libnuma1 \
    libnuma-dev \
    autoconf \
    automake \
    cmake \
    git-core \
    libass-dev \
    libopenjp2-7 \
    libopenjp2-7-dev \
    libopus-dev \
    libfreetype6-dev \
    libgnutls28-dev \
    libmp3lame-dev \
    libsdl2-dev \
    libtool \
    libva-dev \
    libvdpau-dev \
    srt-tools \
    libvorbis-dev \
    libxcb1-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    meson \
    libspeex-dev \
    speex \
    ninja-build \
    pkg-config \
    texinfo \
    zlib1g-dev \
    libx264-dev \
    libgme-dev \
    libsoxr-dev \
    frei0r-plugins-dev \
    librubberband-dev \
    nvidia-cuda-toolkit


RUN pip3 install flask
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz
RUN git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
RUN cd nv-codec-headers && make install && cd -
RUN git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg/
RUN cd ffmpeg/ && ./configure --enable-nonfree --enable-cuda-nvcc --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64 --disable-static --enable-shared --enable-gpl --enable-version3 --enable-static --disable-debug --disable-ffplay --disable-indev=sndio --disable-outdev=sndio --cc=gcc --enable-fontconfig --enable-frei0r --enable-gnutls --enable-gmp --enable-libgme --enable-gray --disable-libaom --enable-libfribidi --enable-libass --enable-libvmaf --enable-libfreetype --enable-libmp3lame --disable-libopencore-amrnb --disable-libopencore-amrwb --enable-libopenjpeg --enable-librubberband --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libvorbis --enable-libopus --enable-libtheora --enable-libvidstab --enable-libvo-amrwbenc --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzvbi --enable-libzimg && make -j 8 && make install
ENTRYPOINT ["/init"]