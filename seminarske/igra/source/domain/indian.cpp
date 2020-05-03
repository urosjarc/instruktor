//
// Created by urosjarc on 1. 05. 20.
//
#include "domain/indian.h"

Indian::Indian(int x, int y, int invincibleRadius, int seeingRadius) : Warrior(x, y, invincibleRadius) {
    this->x = x;
    this->y = y;
    this->seeingRadius = seeingRadius;
}
