#include "../../include/domain/world.h"

#include "../../include/app/utils.h"

using namespace std;

bool World::isDestroyed() {
    float treesDest = 0;

    for (int i = 0; i < this->trees.size(); ++i) {
        if(!this->trees[i]->isAlive) treesDest++;
    }

    return treesDest/this->trees.size() > 0.75;
}
void World::checkWarriorCollisions() {
}
void World::checkFireCollisions() {
    cout << this << " checkFireCollisions"<< endl;
}
void World::nextIteration() {

    for (int i = 0; i < this->badGuys.size(); ++i) {
        int dx = randomInt(-2, 2);
        int dy = randomInt(-2, 2);
        this->badGuys[i]->x += dx; //Todo implement this in .move()
        this->badGuys[i]->y += dy; //Todo implement this in .move()
    }

    for (int i = 0; i < this->indianTeams.size(); ++i) {
        for (int j = 0; j < this->indianTeams[i]->indians.size(); ++j) {
            auto pIndian = this->indianTeams[i]->indians[j];
            int dx = randomInt(-2, 2);
            int dy = randomInt(-2, 2);
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


