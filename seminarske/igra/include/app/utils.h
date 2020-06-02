#ifndef IGRA_UTILS_H
#define IGRA_UTILS_H

int randomInt(int min, int max);
unsigned long mix(unsigned long a, unsigned long b, unsigned long c);

class Point {
public:
    Point(int x, int y);

    int x;
    int y;
};

#endif //IGRA_UTILS_H
