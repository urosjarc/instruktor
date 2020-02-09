#include <stdio.h>
#include <stdlib.h>

#define CALIBRATION_DISTANCE  14.0f
#define CALIBRATION_SIZE 10

float *getRandVolts(int size, float around, float dispersion) {
    float *nums = malloc(size * sizeof(float));

    for (int i = 0; i < size; ++i) {
        float ran = 0.5f - (float) rand() / RAND_MAX;
        float r = ran * dispersion + around;
        nums[i] = r;
    }

    return nums;
}

float volts2distance(float x, float dy) {
    return 13.099f * x * x - 50.588f * x + 58.77 + dy;
}

float calibration(const float x[], int size, float y) {
    float dy = 0;
    for (int i = 0; i < size; ++i) {
        dy += y - volts2distance(x[i], 0);
    }
    dy /= (float) size;

    return dy;
}

float mean(float nums[], int size){
    float mean = 0;
    for (int i = 0; i < size; ++i) {
        mean += nums[i];
    }

    return mean/size;
}

int main() {
    float V = 1.0f;

    /**
     * Na tem odseku dobis volte iz senzorja...
     * Tukaj jaz simuliram pridobivanje voltov iz senzorja tako da dobim random volte okoli vrednosti V z disperzijo 0.2v.
     * CALIBRATION_SIZE je stevilo meritev ki jih bos izvedel na zacetku s katerimi se bo kalibracija zgodila...
     */
    float *volts = getRandVolts(CALIBRATION_SIZE, V, 0.3f);

    /**
     * Na tem odseku se zgodi kalibracija, v funkcijo das vse meritve za kalibracijo, stevilo kalibracij (CALIBRATION_SIZE)
     * in dolzino pri kateri se je kalibracija zgodila... CALIBRATION_DISTANCE.
     */
    const float CAL_V = calibration(volts, CALIBRATION_SIZE, CALIBRATION_DISTANCE);
    const float mean_V = mean(volts, CALIBRATION_SIZE);

    /**
     * In distance je zdaj popravljena!
     */
    printf("Distance (%f): %f\n", V, volts2distance(V, CAL_V));
    printf("Distance (%f): %f", mean_V, volts2distance(mean_V, CAL_V));

    return 0;
}

