#include "../../include/domain/world.h"


using namespace std;

bool World::isDestroyed() {
    std::cout << this << " isDestroyed"<< endl;
    return false;
}
void World::checkWarriorCollisions() {
    cout << this << " checkWarriorCollisions"<< endl;
}
void World::checkFireCollisions() {
    cout << this << " checkFireCollisions"<< endl;
}
void World::nextIteration() {
    cout << this << " nextIteration"<< endl;
}


