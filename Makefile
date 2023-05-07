
CCFLAGS = -march=native -O3 -flto

all: build/synthesizer.so

clean:
	rm build/*

build/synthesizer.so: build/utils.o build/string_instrument.o build/mixer.o build/pa_output.o build/filters.o build/buffers.o
	gcc $(CCFLAGS) $^ --shared -fpic -lm -lpulse-simple -o $@

build/filters.o: filters.c
	gcc $(CCFLAGS) -c $< -o $@

build/buffers.o: buffers.c
	gcc $(CCFLAGS) -c $< -o $@

build/utils.o: utils.c
	gcc $(CCFLAGS) -c $< -o $@

build/pa_output.o: pa_output.c
	gcc $(CCFLAGS) -c $< -o $@

build/mixer.o: mixer.c
	gcc $(CCFLAGS) -c $< -o $@

build/string_instrument.o: string_instrument.c
	gcc $(CCFLAGS) -c $< -o $@

.PHONY: all clean