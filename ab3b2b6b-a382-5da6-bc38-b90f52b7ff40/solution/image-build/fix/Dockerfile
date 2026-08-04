FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates clang libclang-rt-dev make && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone https://github.com/lz4/lz4 src && cd src && git checkout 13a2d9e34ffc4170720ce417c73e396d0ac1471a
WORKDIR /build/src
ENV CC=clang CFLAGS="-fsanitize=address,fuzzer-no-link -g -O1 -fno-omit-frame-pointer"
RUN make -C lib liblz4.a
RUN mkdir -p /out && LIB=$(find /build/src -name liblz4.a|head -1) && PROD=$(find /build/src/ossfuzz -name fuzz_data_producer.c|head -1) && F=$(find /build/src/ossfuzz -name compress_fuzzer.c|head -1) && clang -fsanitize=address,fuzzer -g -O1 -fno-omit-frame-pointer -I /build/src/lib -I /build/src/ossfuzz "$F" "$PROD" /build/src/lib/xxhash.c "$LIB" -o /out/fuzzer
RUN mkdir -p /bin && printf '#!/bin/bash\n/out/fuzzer /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
CMD ["sleep","infinity"]
