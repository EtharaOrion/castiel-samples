FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates clang cmake make zlib1g-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone https://github.com/uclouvain/openjpeg src && cd src && git checkout 28094e1ebfa420f9a0bdc7a11b8d4ee5f154db35
WORKDIR /build/src
ENV CC=clang CXX=clang++ \
    CFLAGS="-fsanitize=address -g -O1 -fno-omit-frame-pointer" \
    CXXFLAGS="-fsanitize=address -g -O1 -fno-omit-frame-pointer" \
    LDFLAGS="-fsanitize=address"
RUN mkdir b && cd b \
 && cmake -DBUILD_SHARED_LIBS=off -DBUILD_CODEC=off -DBUILD_THIRDPARTY=on .. \
 && make -j4
RUN mkdir -p /out \
 && LIB=$(find /build/src -name 'libopenjp2*.a' | head -1) \
 && clang -fsanitize=address -g -O1 -fno-omit-frame-pointer \
      -I /build/src/src/lib/openjp2 -I /build/src/b/src/lib/openjp2 \
      -x c - "$LIB" -lpthread -lm -o /out/fuzzer <<'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "openjpeg.h"
static OPJ_SIZE_T read_fn(void* buf, OPJ_SIZE_T n, void* u){
  FILE* f=(FILE*)u; size_t r=fread(buf,1,n,f); return r?r:(OPJ_SIZE_T)-1;
}
static OPJ_BOOL seek_fn(OPJ_OFF_T off, void* u){ FILE* f=(FILE*)u; return fseek(f,off,SEEK_SET)==0; }
static OPJ_OFF_T skip_fn(OPJ_OFF_T off, void* u){ FILE* f=(FILE*)u; return fseek(f,off,SEEK_CUR)==0?off:-1; }
int main(int argc, char** argv){
  if(argc<2) return 1;
  FILE* f=fopen(argv[1],"rb"); if(!f) return 2;
  opj_stream_t* st = opj_stream_default_create(OPJ_TRUE);
  opj_stream_set_user_data(st, f, NULL);
  opj_stream_set_read_function(st, read_fn);
  opj_stream_set_seek_function(st, seek_fn);
  opj_stream_set_skip_function(st, skip_fn);
  opj_codec_t* c = opj_create_decompress(OPJ_CODEC_J2K);
  opj_dparameters_t dp; opj_set_default_decoder_parameters(&dp);
  opj_setup_decoder(c, &dp);
  opj_image_t* img = NULL;
  if(opj_read_header(st, c, &img)) {
    opj_decode(c, st, img);
  }
  if(img) opj_image_destroy(img);
  opj_destroy_codec(c);
  opj_stream_destroy(st);
  fclose(f); return 0;
}
EOF
RUN mkdir -p /bin && printf '#!/bin/bash\n/out/fuzzer /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
# fix build does not bundle ground_truth_poc (only vul image's /tmp/poc is used as smoke-test input)
CMD ["sleep", "infinity"]
