//
// Created by urosjarc on 1. 05. 20.
//

#include <iostream>
#include "domain/warrior.h"

void Warrior::move() {

    std::cout << this << " move\n";

}

Warrior::Warrior(int x, int y, int invincibleRadius) {
    this->x = x;
    this->y = y;
    this->invincibleRadius = invincibleRadius;
}

