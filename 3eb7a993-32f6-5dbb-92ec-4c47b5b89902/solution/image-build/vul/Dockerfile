FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates clang libclang-rt-dev cmake make && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone https://github.com/c-ares/c-ares src && cd src && git checkout 7d3591ee8a1a63e7748e68e6d880bd1763a32885
WORKDIR /build/src
ENV CC=clang CFLAGS="-fsanitize=address,fuzzer-no-link -g -O1" LDFLAGS="-fsanitize=address"
RUN mkdir bb && cd bb && cmake -DCARES_STATIC=ON -DCARES_SHARED=OFF -DCARES_BUILD_TESTS=OFF .. && make -j4
RUN mkdir -p /out && AH=$(find /build/src -name ares.h|head -1) && FUZZ=$(find /build/src -name ares-test-fuzz.c|head -1) && LIB=$(find /build/src -name 'libcares*.a'|head -1) && clang -fsanitize=address,fuzzer -g -O1 -I "$(dirname "$AH")" -I /build/src/bb -I /build/src/bb/include "$FUZZ" "$LIB" -o /out/fuzzer
RUN mkdir -p /bin && printf '#!/bin/bash\n/out/fuzzer /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
CMD ["sleep","infinity"]
