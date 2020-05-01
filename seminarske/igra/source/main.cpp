#include <iostream>
#include "domain/bad_guy.cpp"
#include "domain/fire.cpp"
#include "domain/hero.cpp"
#include "domain/indian_team.cpp"
#include "domain/indian.cpp"
#include "domain/world.cpp"
#include "domain/warrior.cpp"

int main() {
    std::cout << "Hello, World!" << std::endl;
    auto badGuy = new BadGuy();
    auto fire = new Fire();
    auto hero = new Hero();
    auto indian = new Indian();
    auto indianTeam = new IndianTeam();
    auto tree = new Tree();
    auto warrior = new Warrior();
    auto world = new World();

    world->checkFireCollisions();
    world->checkWarriorCollisions();
    world->nextIteration();

    hero->move(1,1);
    hero->plantTree();

    warrior->move();

    std::cout << badGuy << std::endl;
    std::cout << fire << std::endl;
    std::cout << hero << std::endl;
    std::cout << indian << std::endl;
    std::cout << indianTeam << std::endl;
    std::cout << tree << std::endl;
    std::cout << warrior << std::endl;
    std::cout << world << std::endl;

    return 0;
}
