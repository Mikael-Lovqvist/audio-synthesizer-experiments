#include <math.h>

#define M_TAU (M_PI*2)

#define SAMPLE_RATE			48000
#define BUFFER_SIZE			128

#define SAMPLE_TYPE			float

#define iSAMPLE_RATE		(int) SAMPLE_RATE
#define fSAMPLE_RATE		(float) SAMPLE_RATE
#define sSAMPLE_RATE		(SAMPLE_TYPE) SAMPLE_RATE

typedef SAMPLE_TYPE buffer_segment[128];

