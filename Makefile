CC = gcc
CFLAGS = -shared -fPIC -Wall
LDFLAGS = -lpthread -lm
ALL = Histex.so Profex.so

all: $(ALL)

libfastk.c : gene_core.c
libfastk.h : gene_core.h

Histex.so: Histex.c libfastk.c libfastk.h
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ Histex.c libfastk.c

Profex.so: Profex.c libfastk.c libfastk.h
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ Profex.c libfastk.c

clean:
	rm -f $(ALL)
