//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_INDIAN_H
#define IGRA_INDIAN_H

#include "warrior.h"

class Indian: Warrior {
public:
    Indian(int x, int y, int invincibleRadius = 4, int seeingRadius = 4) : Warrior(x, y, invincibleRadius) {
        this->x = x;
        this->y = y;
        this->seeingRadius = seeingRadius;
    }
    int seeingRadius;
    bool panicMode = false;
};

#endif //IGRA_INDIAN_H
