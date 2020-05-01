//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_HERO_H
#define IGRA_HERO_H

#include "indian_team.h"
#include "tree.h"
#include "warrior.h"

class Hero: Warrior {
public:
    bool isAlive;
    char name[10];
    int reputation;

    Tree plantTree();
    void move(int dx, int dy);
};

#endif //IGRA_HERO_H
