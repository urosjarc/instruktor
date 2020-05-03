//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_FIRE_H
#define IGRA_FIRE_H

class Fire {
public:
    Fire(int x, int y) {
        this->x = x;
        this->y = y;
    }

    int x;
    int y;
    float radius = 0;
};

#endif //IGRA_FIRE_H
