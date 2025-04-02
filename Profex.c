/*********************************************************************************************\
 *
 *  Example code for opening and fetching compressed profiles produced by FastK
 *
 *  Author:  Gene Myers
 *  Date  :  October, 2020
 *
 *********************************************************************************************/

// modified by: Yoshi Suzuki

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <math.h>

#include "libfastk.h"

typedef struct {
  uint16 *profile;
  int length;
  int kmer;
} Profile;

static Profile_Index *P;
static Profile *ret;
static int pmax = 20000;

void open_profile(char *source) {
  P = Open_Profiles(source);
  if (P == NULL) {
    fprintf(stderr, "Cannot open %s\n", source);
    exit(1);
  }
  ret = Malloc(sizeof(Profile), "Single profile");
  ret->profile = Malloc(pmax * sizeof(uint16), "Profile array");
}

Profile *load_profile(int64 id) {
  if (id <= 0 || id > P->nbase[P->nparts - 1]) {
    fprintf(stderr, "Id %lld is out of range\n", id);
    exit(1);
  }

  int plen = Fetch_Profile(P, id - 1, pmax, ret->profile);
  if (plen > pmax) {
    pmax = 1.2 * plen + 1000;
    ret->profile =
        Realloc(ret->profile, pmax * sizeof(uint16), "Profile array");
    Fetch_Profile(P, id - 1, pmax, ret->profile);
  }
  ret->length = plen;
  ret->kmer = P->kmer;
  return ret;
}

void free_profile() {
  Free_Profiles(P);
  free(ret->profile);
  free(ret);
}
