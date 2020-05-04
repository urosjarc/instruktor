#include <cmath>
#include <iostream>

#include "domain/world.h"
#include "app/utils.h"

bool World::isDestroyed() {
    float treesDest = 0;

    for (int i = 0; i < this->trees.size(); ++i) {
        if(!this->trees[i]->isAlive) treesDest++;
    }

    return treesDest/this->trees.size() > 0.75;
}
void World::checkWarriorCollisions() {
    /**
     * Bad guys invincible status
     */
    for (int i = 0; i < this->badGuys.size(); ++i) {
        bool isFound = false;
        auto pBadGuy0 = this->badGuys[i];
        for (int j = 0; j < this->badGuys.size(); ++j) {
            auto pBadGuy1 = this->badGuys[j];
            float dx = pBadGuy0->x - pBadGuy1->x;
            float dy = pBadGuy0->y - pBadGuy1->y;
            float dist = pow(pow(dx, 2) + pow(dy, 2), 0.5);
            if(i!=j && pBadGuy0->invincibleRadius >= dist){
                pBadGuy0->invincible = true;
                isFound = true;
                break;
            }
        }
        if(!isFound) pBadGuy0->invincible = false;
    }
}
void World::checkFireCollisions() {
    std::cout << this << " checkFireCollisions\n";
}
void World::nextIteration() {

    for (int i = 0; i < this->badGuys.size(); ++i) {
        int dx = randomInt(-1, 1);
        int dy = randomInt(-1, 1);
        this->badGuys[i]->x += dx; //Todo implement this in .move()
        this->badGuys[i]->y += dy; //Todo implement this in .move()
    }

    for (int i = 0; i < this->indianTeams.size(); ++i) {
        for (int j = 0; j < this->indianTeams[i]->indians.size(); ++j) {
            auto pIndian = this->indianTeams[i]->indians[j];
            int dx = randomInt(-1, 1);
            int dy = randomInt(-1, 1);
            pIndian->x += dx; //Todo implement this in .move()
            pIndian->y += dy; //Todo implement this in .move()
        }
    }

    for (int i = 0; i < this->fires.size(); ++i) {
        this->fires[i]->radius += 0.1 * this->fireIndex;
    }
    this->checkWarriorCollisions();
    this->checkFireCollisions();
}

World::World(Hero *hero, int fireIndex, int badGuysIndex, int indiansIndex, int waterIndex, int width, int height,
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


