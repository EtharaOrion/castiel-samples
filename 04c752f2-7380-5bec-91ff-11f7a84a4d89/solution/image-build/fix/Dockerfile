FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates clang libclang-rt-dev make autoconf automake libtool && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone https://github.com/PCRE2Project/pcre2 src && cd src && git checkout 5f77d022733a5b7e2ff1e3d80b547c0d89811efe
WORKDIR /build/src
ENV CC=clang CFLAGS="-fsanitize=address,fuzzer-no-link -g -O1" LDFLAGS="-fsanitize=address"
RUN if [ -f autogen.sh ]; then ./autogen.sh; fi && ./configure --disable-shared --enable-static --enable-jit=auto && make -j4
RUN mkdir -p /out && HARN=$(find /build/src -name pcre2_fuzzsupport.c|head -1) && LIB=$(find /build/src -name 'libpcre2-8*.a'|head -1) && clang -fsanitize=address,fuzzer -g -O1 -DPCRE2_CODE_UNIT_WIDTH=8 -I /build/src/src "$HARN" "$LIB" -o /out/fuzzer
RUN mkdir -p /bin && printf '#!/bin/bash\n/out/fuzzer /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
CMD ["sleep","infinity"]
