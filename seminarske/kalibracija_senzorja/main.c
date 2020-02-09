#include <stdio.h>
#include <stdlib.h>

#define CALIBRATION_DISTANCE  14.0f
#define CALIBRATION_SIZE 20

float *getRandVolts(int size, float around, float dispersion) {
    float *nums = malloc(size * sizeof(float));

    for (int i = 0; i < size; ++i) {
        float ran = 0.5f - (float) rand() / RAND_MAX;
        float r = ran * dispersion + around;
        nums[i] = r;
    }

    return nums;
}

float volts2distance(float x, float dx) {
    x += dx;
    return 13.099f * x * x - 50.588f * x + 58.77;
}

float calibration(float x[], int size, float y) {
    float meanX = 0;
    for (int i = 0; i < size; ++i) {
        meanX += x[i];
    }
    meanX /= (float) size;

    float dx=0;
    float d = 1e-5f;
    float dy1, dy2, k;
    do {
        dy1 = volts2distance(meanX,dx);
        dy2 = volts2distance(meanX,dx+d);
        k = (dy2-dy1)/(d);
        dx += (y - dy1)/k;

    } while ((y-dy1)*(y-dy1) >= 0.00001);

    printf("%f\n", meanX);
    printf("%f\n", volts2distance(meanX, dx));

    return dx;
}

int main() {
    float V = 1.0f;

    /**
     * Na tem odseku dobis volte iz senzorja...
     * Tukaj jaz simuliram pridobivanje voltov iz senzorja tako da dobim random volte okoli vrednosti V z disperzijo 0.2v.
     * CALIBRATION_SIZE je stevilo meritev ki jih bos izvedel na zacetku s katerimi se bo kalibracija zgodila...
     */
    float *volts = getRandVolts(CALIBRATION_SIZE, V, 0.2f);

    /**
     * Na tem odseku se zgodi kalibracija, v funkcijo das vse meritve za kalibracijo, stevilo kalibracij (CALIBRATION_SIZE)
     * in dolzino pri kateri se je kalibracija zgodila... CALIBRATION_DISTANCE.
     */
    const float CAL_V = calibration(volts, CALIBRATION_SIZE, CALIBRATION_DISTANCE);

    /**
     * Z to funkcijo pa pridobis volte, V je meritev iz senzorja, CAL_V pa je korekcijski faktor za kalibracijo!
     */
    float distance = volts2distance(V, CAL_V);

    /**
     * In distance je zdaj popravljena!
     */
    printf("Distance: %f", distance);

    return 0;
}

