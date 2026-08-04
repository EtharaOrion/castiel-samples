FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates clang libclang-rt-dev cmake make pkg-config python3 ragel gperf && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone https://github.com/harfbuzz/harfbuzz src && cd src && git checkout 72d8f76368b264a42fe58438fe15811d458a7935
WORKDIR /build/src
ENV CC=clang CXX=clang++ CFLAGS="-fsanitize=address,undefined,fuzzer-no-link -g -O1" CXXFLAGS="-fsanitize=address,undefined,fuzzer-no-link -g -O1" LDFLAGS="-fsanitize=address,undefined"
RUN mkdir b && cd b && cmake -DHB_HAVE_GLIB=OFF -DHB_HAVE_FREETYPE=OFF -DBUILD_SHARED_LIBS=OFF .. && make -j4
RUN mkdir -p /out && FUZZ=$(find /build/src -name 'hb-shape-fuzzer.cc' | head -1) && LIB=$(find /build/src -name 'libharfbuzz*.a' | head -1) && clang++ -fsanitize=address,undefined,fuzzer -g -O1 -I /build/src/src "$FUZZ" "$LIB" -lpthread -o /out/fuzzer
RUN mkdir -p /bin && printf '#!/bin/bash\n/out/fuzzer /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
CMD ["sleep", "infinity"]
