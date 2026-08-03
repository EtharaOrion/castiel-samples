FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates clang make autoconf automake libtool && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone https://github.com/PCRE2Project/pcre2 src && cd src && git checkout 1e78b77382564b4cc9991e486652d4b105d8ee35
WORKDIR /build/src
ENV CC=clang \
    CFLAGS="-fsanitize=address -g -O1 -fno-omit-frame-pointer" \
    LDFLAGS="-fsanitize=address"
RUN if [ -f autogen.sh ]; then ./autogen.sh; fi \
 && ./configure --disable-shared --enable-static --enable-jit=auto \
 && make -j4
RUN mkdir -p /out \
 && LIB=$(find /build/src -name 'libpcre2-8*.a' | head -1) \
 && HARN=$(find /build/src -name 'pcre2_fuzzsupport.c' | head -1) \
 && if [ -n "$HARN" ]; then \
      clang -fsanitize=address -g -O1 -fno-omit-frame-pointer -DPCRE2_CODE_UNIT_WIDTH=8 -I /build/src/src "$HARN" "$LIB" -o /out/fuzzer ; \
    else \
      clang -fsanitize=address -g -O1 -fno-omit-frame-pointer -DPCRE2_CODE_UNIT_WIDTH=8 -I /build/src/src -x c - "$LIB" -o /out/fuzzer <<'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pcre2.h>
int main(int argc, char** argv){
  if(argc<2) return 1;
  FILE* f=fopen(argv[1],"rb"); if(!f) return 2;
  fseek(f,0,SEEK_END); long n=ftell(f); fseek(f,0,SEEK_SET);
  unsigned char* b=(unsigned char*)malloc(n+1); if(fread(b,1,n,f)!=(size_t)n){free(b);return 3;} fclose(f); b[n]=0;
  int errnum=0; PCRE2_SIZE erroffset=0;
  pcre2_code* re = pcre2_compile(b,(PCRE2_SIZE)n, 0, &errnum, &erroffset, NULL);
  if(re){
    pcre2_match_data* md = pcre2_match_data_create_from_pattern(re, NULL);
    pcre2_match(re, b, (PCRE2_SIZE)n, 0, 0, md, NULL);
    pcre2_match_data_free(md);
    pcre2_code_free(re);
  }
  free(b); return 0;
}
EOF
    fi
RUN mkdir -p /bin && printf '#!/bin/bash\n/out/fuzzer /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
# ground_truth_poc not bundled; the prebuilt ECR image already contains /tmp/poc baked in
CMD ["sleep", "infinity"]
