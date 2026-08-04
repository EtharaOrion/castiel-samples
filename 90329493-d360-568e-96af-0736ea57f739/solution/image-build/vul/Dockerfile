FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates clang libclang-rt-dev cmake make zlib1g-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone https://github.com/uclouvain/openjpeg src && cd src && git checkout cc893a4ebfaf8c42cf1221ac82c83df91e77340b
WORKDIR /build/src
ENV CC=clang CXX=clang++ CFLAGS="-fsanitize=address,fuzzer-no-link -g -O1" CXXFLAGS="-fsanitize=address,fuzzer-no-link -g -O1" LDFLAGS="-fsanitize=address"
RUN mkdir bb && cd bb && cmake -DBUILD_SHARED_LIBS=off -DBUILD_CODEC=off -DBUILD_THIRDPARTY=on .. && make -j4
RUN mkdir -p /out && FUZZ=$(find /build/src -name 'opj_decompress_fuzzer.c*'|head -1) && LIB=$(find /build/src -name 'libopenjp2*.a'|head -1) && clang++ -fsanitize=address,fuzzer -g -O1 -DOPJ_STATIC -I /build/src/src/lib/openjp2 -I /build/src/bb/src/lib/openjp2 "$FUZZ" "$LIB" -lpthread -lm -o /out/fuzzer
RUN mkdir -p /bin && printf '#!/bin/bash\n/out/fuzzer /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
CMD ["sleep","infinity"]
