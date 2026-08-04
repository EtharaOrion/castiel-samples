FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates clang libclang-rt-dev cmake make && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone https://github.com/open-source-parsers/jsoncpp src && cd src && git checkout c4bc6da87d9588032a3ce54abf59c7548af58f7f
WORKDIR /build/src
ENV CC=clang CXX=clang++ CFLAGS="-fsanitize=address,fuzzer-no-link -g -O1 -fno-omit-frame-pointer" CXXFLAGS="-fsanitize=address,fuzzer-no-link -g -O1 -fno-omit-frame-pointer" LDFLAGS="-fsanitize=address"
RUN mkdir bb && cd bb && cmake -DBUILD_SHARED_LIBS=OFF -DJSONCPP_WITH_TESTS=OFF -DJSONCPP_WITH_POST_BUILD_UNITTEST=OFF .. && make -j4
RUN mkdir -p /out && FUZZ=$(find /build/src -name fuzz.cpp -path '*test_lib_json*'|head -1) && LIB=$(find /build/src -name 'libjsoncpp*.a'|head -1) \
 && clang++ -fsanitize=address,fuzzer -g -O1 -fno-omit-frame-pointer -I /build/src/include "$FUZZ" "$LIB" -o /out/fuzzer
RUN mkdir -p /bin && printf '#!/bin/bash\n/out/fuzzer /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
CMD ["sleep","infinity"]
