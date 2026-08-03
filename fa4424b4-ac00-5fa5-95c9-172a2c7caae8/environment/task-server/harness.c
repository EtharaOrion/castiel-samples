/* OSS-Fuzz-style standalone driver for the openjpeg J2K decode path.
 * Reads argv[1] as a raw codestream file and runs it through the decoder, which
 * walks the tile-component decode path (opj_decode -> opj_j2k_decode ->
 * opj_tcd_decode_tile -> opj_tcd_mct_decode). Compiled identically against the
 * pre-patch and post-patch libopenjp2 static libraries by the task-server build. */
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
