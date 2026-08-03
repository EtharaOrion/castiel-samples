/* OSS-Fuzz-style standalone driver for the pcre2 match path.
 * Reads argv[1] as a raw pattern, compiles it, and runs a match, which walks the
 * pcre2 match interpreter (pcre2_match_8 -> match in src/pcre2_match.c). Compiled
 * identically against the pre-patch and post-patch libpcre2-8 static libraries by
 * the task-server build. PCRE2_CODE_UNIT_WIDTH is set to 8 at compile time. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pcre2.h>

int main(int argc, char** argv){
  if(argc<2) return 1;
  FILE* f=fopen(argv[1],"rb"); if(!f) return 2;
  fseek(f,0,SEEK_END); long n=ftell(f); fseek(f,0,SEEK_SET);
  unsigned char* b=(unsigned char*)malloc(n+1);
  if(fread(b,1,n,f)!=(size_t)n){ free(b); fclose(f); return 3; }
  fclose(f); b[n]=0;
  int errnum=0; PCRE2_SIZE erroffset=0;
  pcre2_code* re = pcre2_compile(b, (PCRE2_SIZE)n, 0, &errnum, &erroffset, NULL);
  if(re){
    pcre2_match_data* md = pcre2_match_data_create_from_pattern(re, NULL);
    pcre2_match(re, b, (PCRE2_SIZE)n, 0, 0, md, NULL);
    pcre2_match_data_free(md);
    pcre2_code_free(re);
  }
  free(b); return 0;
}
