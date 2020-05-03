//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_BAD_GUY_H
#define IGRA_BAD_GUY_H

#include "indian_team.h"

class BadGuy: Warrior {
public:
    BadGuy(int x, int y, int invincibleRadius = 4) : Warrior(x, y, invincibleRadius) {
        this->x = x;
        this->y = x;
    }

};

#endif //IGRA_BAD_GUY_H
