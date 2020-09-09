FROM python:3-alpine

# get ffplayout engine and install all dependencies
RUN cd /opt && \
    wget "https://github.com/ffplayout/ffplayout-engine/archive/master.zip" && \
    unzip 'master.zip' && \
    mv 'ffplayout-engine-master' 'ffplayout-engine' && \
    rm master.zip && \
    cd ffplayout-engine && \
    pip install -r requirements-base.txt && \
    mkdir /etc/ffplayout

# install build tools, ffmpeg dependencies and compile ffmpeg
RUN apk update && \
    apk add --no-cache autoconf automake build-base cmake gcc libtool gperf nasm yasm \
        expat-dev zlib-dev openssl-dev fontconfig-dev libxml2-dev lame-dev \
        gnu-libiconv libpng-dev fribidi-dev zeromq-dev freetype-dev opus-dev \
        fdk-aac-dev libvpx-dev libass-dev x264-dev x265-dev && \
    cd /opt && \
    wget "https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2" && \
    tar xfvj ffmpeg-snapshot.tar.bz2 && \
    rm ffmpeg-snapshot.tar.bz2 && \
    cd ffmpeg && \
    ./configure --prefix="/usr/local/" --disable-debug --disable-doc --enable-gpl \
    --enable-version3 --enable-nonfree --enable-runtime-cpudetect --enable-fontconfig \
    --enable-openssl --enable-libass --enable-libfdk-aac --enable-libfreetype \
    --enable-libfribidi --enable-libmp3lame --enable-libopus --enable-libvpx \
    --enable-libx264 --enable-libx265 --enable-libzmq && \
    make -j $(nproc | awk '{print $1 / 2}') && \
    make install && \
    cd .. && \
    rm -rf ffmpeg && \
    # cleanup
    apk del autoconf automake build-base cmake gcc libtool gperf nasm yasm

WORKDIR /opt/ffplayout-engine
EXPOSE 5555

CMD [ "/opt/ffplayout-engine/ffplayout.py" ]
