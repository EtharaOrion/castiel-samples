FROM --platform=linux/amd64 ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates clang libclang-rt-dev cmake make pkg-config python3 \
    autoconf automake libtool gtk-doc-tools ragel gperf \
    libfreetype-dev libglib2.0-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone https://github.com/harfbuzz/harfbuzz src && cd src && git checkout e940530c9723c3a581a5d5b31e5f419865dd6cc7
WORKDIR /build/src
ENV CC=clang CXX=clang++ \
    CFLAGS="-fsanitize=address,undefined -g -O1 -fno-omit-frame-pointer" \
    CXXFLAGS="-fsanitize=address,undefined -g -O1 -fno-omit-frame-pointer" \
    LDFLAGS="-fsanitize=address,undefined"
RUN if [ -f autogen.sh ]; then ./autogen.sh --with-glib=no --with-freetype=no --with-cairo=no --disable-shared --enable-static; \
    else mkdir b && cd b && cmake -DHB_HAVE_GLIB=OFF -DHB_HAVE_FREETYPE=OFF -DBUILD_SHARED_LIBS=OFF .. ; fi \
 && make -j4 || make -k -j1 || true
RUN mkdir -p /out \
 && HARN=$(find /build/src -name 'hb-shape-fuzzer.cc' -o -name 'hb-subset-fuzzer.cc' | head -1) \
 && LIB=$(find /build/src -name 'libharfbuzz*.a' | head -1) \
 && clang++ -fsanitize=address,undefined -g -O1 -fno-omit-frame-pointer \
      -I /build/src/src "$HARN" "$LIB" -lpthread -o /out/harness || \
    clang++ -fsanitize=address,undefined -g -O1 \
      -I /build/src/src /build/src/src/*.cc -DHB_NO_MT \
      -x c++ - -lpthread -o /out/harness <<'EOF'
#include <hb.h>
#include <cstdio>
int main(int argc, char** argv){
  if(argc<2) return 1;
  FILE* f=fopen(argv[1],"rb"); if(!f) return 2;
  fseek(f,0,SEEK_END); long n=ftell(f); fseek(f,0,SEEK_SET);
  char* b=(char*)malloc(n); if(fread(b,1,n,f)!=(size_t)n){return 3;} fclose(f);
  hb_blob_t* blob=hb_blob_create(b,n,HB_MEMORY_MODE_READONLY,nullptr,nullptr);
  hb_face_t* face=hb_face_create(blob,0);
  hb_font_t* font=hb_font_create(face);
  hb_buffer_t* buf=hb_buffer_create();
  hb_buffer_add_utf8(buf,"abc",-1,0,-1);
  hb_buffer_guess_segment_properties(buf);
  hb_shape(font,buf,nullptr,0);
  hb_buffer_destroy(buf); hb_font_destroy(font); hb_face_destroy(face); hb_blob_destroy(blob); free(b);
  return 0;
}
EOF
RUN mkdir -p /bin && printf '#!/bin/bash\n/out/harness /tmp/poc\n' > /bin/arvo && chmod +x /bin/arvo
CMD ["sleep", "infinity"]
