//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_HERO_H
#define IGRA_HERO_H

#include "indian_team.h"
#include "tree.h"
#include "warrior.h"
#include "app/utils.h"
#include "iostream"

class Hero : public Warrior {
public:
    Hero(int x, int y, int invincibleRadius = 4);

    bool isAlive = true;
    std::string name = "Neznanec";
    int reputation = 0;

    std::vector<Point *> history{};

    Tree *plantTree(int x, int y);

    void move(int dx, int dy);
};

#endif //IGRA_HERO_H
