
CCFLAGS = -march=native -O3 -flto

all: build/t1.so

clean:
	rm build/*

build/t1.so: build/t1.o build/string_instrument.o build/mixer.o build/pa_output.o
	gcc $(CCFLAGS) $^ --shared -fpic -lm -lpulse-simple -o $@

build/t1.o: t1.c
	gcc $(CCFLAGS) -c $< -o $@

build/pa_output.o: pa_output.c
	gcc $(CCFLAGS) -c $< -o $@

build/mixer.o: mixer.c
	gcc $(CCFLAGS) -c $< -o $@

build/string_instrument.o: string_instrument.c
	gcc $(CCFLAGS) -c $< -o $@

.PHONY: all clean