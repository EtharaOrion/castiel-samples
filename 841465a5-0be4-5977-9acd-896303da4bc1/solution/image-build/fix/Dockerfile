# Fixed runner image for jsoncpp OSS-Fuzz issue 21916. Identical to vul/Dockerfile
# EXCEPT the checked-out commit: 6aba23f (#1180, "Fixes Oss-Fuzz issue: 21916"),
# which adds the `(end_ - begin_) >= 3` bounds check before the BOM strncmp in
# OurReader::skipBom. Same harness, same ASAN flags.
FROM --platform=linux/amd64 ubuntu:22.04@sha256:0e0a0fc6d18feda9db1590da249ac93e8d5abfea8f4c3c0c849ce512b5ef8982

RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates clang cmake make && rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN git clone https://github.com/open-source-parsers/jsoncpp src \
 && cd src && git checkout 6aba23f4a8628d599a9ef7fa4811c4ff6e4070e2

WORKDIR /build/src
ENV CC=clang CXX=clang++ \
    CXXFLAGS="-fsanitize=address -g -O1 -fno-omit-frame-pointer -stdlib=libstdc++" \
    LDFLAGS="-fsanitize=address"
RUN mkdir b && cd b \
 && cmake -DJSONCPP_WITH_TESTS=OFF -DBUILD_SHARED_LIBS=OFF -DJSONCPP_WITH_POST_BUILD_UNITTEST=OFF .. \
 && make -j4

RUN mkdir -p /out \
 && LIB=$(find /build/src -name 'libjsoncpp*.a' | head -1) \
 && clang++ -fsanitize=address -g -O1 -fno-omit-frame-pointer \
      -I /build/src/include -x c++ - -x none "$LIB" -lpthread -o /out/harness <<'EOF'
#include <json/json.h>
#include <fstream>
#include <iterator>
#include <vector>
#include <string>
#include <memory>
int main(int argc, char** argv) {
  if (argc < 2) return 1;
  std::ifstream f(argv[1], std::ios::binary);
  std::vector<char> buf((std::istreambuf_iterator<char>(f)),
                        std::istreambuf_iterator<char>());
  const char* begin = buf.data();
  const char* end = begin + buf.size();
  Json::CharReaderBuilder rb;
  std::unique_ptr<Json::CharReader> cr(rb.newCharReader());
  Json::Value v; std::string err;
  cr->parse(begin, end, &v, &err);
  return 0;
}
EOF

RUN mkdir -p /bin && printf '#!/bin/bash\n/out/harness /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
CMD ["sleep", "infinity"]
