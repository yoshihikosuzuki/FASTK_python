/*******************************************************************************************
 *
 *  Example code for reading and displatying a kmer histogram produced by FastK.
 *
 *  Author:  Gene Myers
 *  Date  :  October 2020
 *
 *******************************************************************************************/

// modified by: Yoshi Suzuki

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "libfastk.h"

static inline void mycpy(int64 *a, int64 *b, int n) {
  while (n--) *a++ = *b++;
}

int64 *load_hist(char *source, int HIST_LOW, int HIST_HGH, int UNIQUE) {
  Histogram *H;
  int64 *hist;

  //  Process arguments
  {
    if (HIST_LOW < 1 || HIST_LOW > 0x7fff) {
      fprintf(stderr, "Histogram count %d is out of range\n", HIST_LOW);
      exit(1);
    }
    if (HIST_LOW > HIST_HGH) {
      fprintf(stderr, "Histogram range is invalid\n");
      exit(1);
    }
    if (HIST_HGH > 0x7fff) HIST_HGH = 0x7fff;
  }

  //  Load histogram into "hist"
  {
    H = Load_Histogram(source);
    if (H == NULL) {
      fprintf(stderr, "Cannot open %s\n", source);
      exit(1);
    }

    if (HIST_LOW < H->low || HIST_HGH > H->high) {
      fprintf(
          stderr,
          "Range of histogram, [%d,%d], does not superset requested range\n",
          H->low, H->high);
      exit(1);
    }

    Modify_Histogram(H, HIST_LOW, HIST_HGH, UNIQUE);

    hist = Malloc((HIST_HGH - HIST_LOW + 1) * sizeof(int64),
                  "Allocating histogram");
    mycpy(hist, H->hist + HIST_LOW, HIST_HGH - HIST_LOW + 1);
  }

  Free_Histogram(H);
  return hist;
}

void free_hist(int64 *hist) { free(hist); }
