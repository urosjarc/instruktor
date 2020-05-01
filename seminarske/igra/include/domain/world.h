//
// Created by urosjarc on 1. 05. 20.
//

#ifndef IGRA_WORLD_H
#define IGRA_WORLD_H

#include <vector>
#include "hero.h"
#include "fire.h"
#include "bad_guy.h"

class World {
public:
    int fireIndex;
    int badGuysIndex;
    int indiansIndex;
    int waterIndex;
    int width;
    int height;
    int secondsToLive;

    Hero hero;
    IndianTeam indianTeams[10];
    std::vector<Fire*> fires;
    std::vector<Tree*> trees;
    std::vector<BadGuy*> badGuys;

    bool isDestroyed();
    void checkWarriorCollisions();
    void checkFireCollisions();
    void nextIteration();
};

#endif //IGRA_WORLD_H
