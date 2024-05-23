CFLAGS = -O2 -fpic -pie

all:
	gcc stereFlow.c -o stereFlow.o $(CFLAGS) -c
	gcc -shared -fPIC -o libStereFlow.so stereFlow.o
