//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_HERO_H
#define IGRA_HERO_H

#include "indian_team.h"
#include "tree.h"
#include "warrior.h"

class Hero: public Warrior {
public:
    Hero(int x, int y, int invincibleRadius = 4) : Warrior(x, y, invincibleRadius) {
        this->x = x;
        this->y = y;
    }
    bool isAlive = true;
    char name[10];
    int reputation = 0;

    Tree* plantTree(int x, int y);
    void move(int dx, int dy);
};

#endif //IGRA_HERO_H
