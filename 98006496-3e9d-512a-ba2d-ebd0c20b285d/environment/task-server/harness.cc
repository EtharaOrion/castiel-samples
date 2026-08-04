/* OSS-Fuzz-style standalone driver for the harfbuzz shape path.
 * Reads argv[1] as a raw font blob, creates a face and font, and shapes a short
 * buffer. Loading the face lazily sanitizes the font tables, which walks the AAT
 * kerx table sanitizer (AAT::kerx::sanitize -> AAT::KerxTable::sanitize ->
 * AAT::KerxSubTableFormat1::sanitize in src/hb-aat-layout-kerx-table.hh).
 * Compiled identically against the pre-patch and post-patch libharfbuzz static
 * libraries by the task-server build. */
#include <hb.h>
#include <cstdio>
#include <cstdlib>

int main(int argc, char** argv){
  if(argc<2) return 1;
  FILE* f=fopen(argv[1],"rb"); if(!f) return 2;
  fseek(f,0,SEEK_END); long n=ftell(f); fseek(f,0,SEEK_SET);
  char* b=(char*)malloc(n); if(!b){ fclose(f); return 4; }
  if(fread(b,1,n,f)!=(size_t)n){ free(b); fclose(f); return 3; }
  fclose(f);
  hb_blob_t* blob=hb_blob_create(b,n,HB_MEMORY_MODE_READONLY,nullptr,nullptr);
  hb_face_t* face=hb_face_create(blob,0);
  hb_font_t* font=hb_font_create(face);
  hb_buffer_t* buf=hb_buffer_create();
  hb_buffer_add_utf8(buf,"abc",-1,0,-1);
  hb_buffer_guess_segment_properties(buf);
  hb_shape(font,buf,nullptr,0);
  hb_buffer_destroy(buf); hb_font_destroy(font); hb_face_destroy(face); hb_blob_destroy(blob);
  free(b);
  return 0;
}
