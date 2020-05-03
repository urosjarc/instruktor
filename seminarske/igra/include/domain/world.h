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
    World(
        Hero* hero,
        int fireIndex,
        int badGuysIndex,
        int indiansIndex,
        int waterIndex,
        int width,
        int height,
        int secondsToLive);

    int fireIndex;
    int badGuysIndex;
    int indiansIndex;
    int waterIndex;
    int width;
    int height;
    int secondsToLive;

    Hero* hero;
    std::vector<IndianTeam*> indianTeams;
    std::vector<Fire*> fires;
    std::vector<Tree*> trees;
    std::vector<BadGuy*> badGuys;

    bool isDestroyed();
    void checkWarriorCollisions();
    void checkFireCollisions();
    void nextIteration();
};

#endif //IGRA_WORLD_H
