//
// Created by urosjarc on 1. 05. 20.
//

#include <iostream>
#include "domain/warrior.h"

using namespace std;

void Warrior::move() {

    cout << this << " move" << endl;

}

Warrior::Warrior(int x, int y, int invincibleRadius) {
    this->x = x;
    this->y = y;
    this->invincibleRadius = invincibleRadius;
}

