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
        int secondsToLive) {

        this->hero = hero;
        this->fireIndex = fireIndex;
        this->badGuysIndex = badGuysIndex;
        this->indiansIndex = indiansIndex;
        this->waterIndex = waterIndex;
        this->width = width;
        this->height = height;
        this->secondsToLive = secondsToLive;

        for (int x = 0; x < this->width; ++x) {
            for (int y = 0; y < this->height; ++y) {
                auto tree = new Tree(x, y);
                this->trees.push_back(tree);
            }
        }
    }

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
