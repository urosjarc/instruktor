
#include "../../include/app/terminal.h"
#include "simbols.cpp"
#include "../domain/indian_team.cpp"

void Terminal::draw() {
    for (int y = 0; y < this->world->height; ++y) {
        for (int x = 0; x < this->world->width; ++x) {
            std::cout << (char) tree;
        }
        std::cout << endl;
    }
}

void Terminal::input() {
    int dx, dy;

    std::cout << "Vnesi hero->dx: " << std::endl;
    std::cin >> dx;

    std::cout << "Vnesi hero->dy: " << std::endl;
    std::cin >> dy;

    this->world->hero->move(dx, dy);
}

void Terminal::createWorld() {
    //Branje iz datoteke...
    //Na podlagi datotek ustvari domenski prostor...

    /*
     * USTVARJANJE TESTNEGA DOMENSTEGA PROSTORA
     */

    auto hero = new Hero(20, 20);

    auto world = new World(hero, 1, 1, 1, 1, 40, 15, 2 * 60);

    auto fire = new Fire(25, 30);
    auto badguy0 = new BadGuy(15, 15);
    auto badguy1 = new BadGuy(25, 25);

    auto indianTeam0 = new IndianTeam(10, 10);
    auto indianTeam1 = new IndianTeam(5, 5);
    auto indianTeam2 = new IndianTeam(30, 30);

    world->badGuys.push_back(badguy0);
    world->badGuys.push_back(badguy1);

    world->indianTeams.push_back(indianTeam0);
    world->indianTeams.push_back(indianTeam1);
    world->indianTeams.push_back(indianTeam2);

    world->fires.push_back(fire);

    this->world = world;

    /**
     * ========================================
     */
}
