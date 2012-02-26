CFLAGS=-O -Wall -Wextra -Werror -std=c99 -pedantic \
	-Wshadow -Wpointer-arith -Wcast-qual \
	-Wstrict-prototypes -Wmissing-prototypes \
	-Wconversion \
	-Wno-unused-parameter \
	-DDEBUG

minivm: minivm.c
	$(CC) $(CFLAGS) $< -o $@
