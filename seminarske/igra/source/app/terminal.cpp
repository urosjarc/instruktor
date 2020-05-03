
#include "math.h"
#include "../../include/app/terminal.h"
#include "simbols.cpp"
#include "../domain/indian_team.cpp"

void Terminal::draw() {
    for (int y = 0; y < this->world->height; ++y) {
        for (int x = 0; x < this->world->width; ++x) {
            if (x == this->world->hero->x && y == this->world->hero->y) {
                std::cout << (char) hero;
                continue;
            }

            /**
             * Draw badguys
             */
            bool isBadGuy = false;
            for (int i = 0; i < this->world->badGuys.size(); ++i) {
                if (x == this->world->badGuys[i]->x && y == this->world->badGuys[i]->y) {
                    std::cout << (char) badGuy;
                    isBadGuy = true;
                    break;
                }
            }
            if (isBadGuy) continue;

            /**
             * Draw indian teams & indians
             */
            bool isIndianTeam = false;
            for (int i = 0; i < this->world->indianTeams.size(); ++i) {
                if (x == this->world->indianTeams[i]->x && y == this->world->indianTeams[i]->y) {
                    std::cout << (char) indianTeam;
                    isIndianTeam = true;
                    break;
                }

                for (int j = 0; j < this->world->indianTeams[i]->indians.size(); ++j) {
                    auto pIndian = this->world->indianTeams[i]->indians[j];
                    if(pIndian->x == x && pIndian->y == y) {
                        std::cout << (char) indian;
                        break;
                    }
                }
            }
            if (isIndianTeam) continue;

            /**
             * Draw fire
             */
            bool isFire = false;
            for (int i = 0; i < this->world->fires.size(); ++i) {
                float dx = this->world->fires[i]->x - x;
                float dy = this->world->fires[i]->y - y;
                float dist = pow(pow(dx, 2) + pow(dy, 2), 0.5); // (dx^2 + dy^2)^(1/2)

                if (dist < this->world->fires[i]->radius) {
                    std::cout << (char) fire;
                    isFire = true;
                    break;
                }
            }
            if (isFire) continue;

            std::cout << (char) tree;
        }
        std::cout << endl;
    }
}

void Terminal::input() {
    int dx, dy;

    std::cout << "Vnesi hero->dx: ";
    std::cin >> dx;

    std::cout << "Vnesi hero->dy: ";
    std::cin >> dy;

    this->world->hero->move(dx, dy);
}

void Terminal::createWorld() {
    //Branje iz datoteke...
    //Na podlagi datotek ustvari domenski prostor...

    /*
     * USTVARJANJE TESTNEGA DOMENSTEGA PROSTORA
     */

    auto hero = new Hero(20, 7);

    auto world = new World(hero, 1, 1, 1, 1, 40, 15, 2 * 60);

    auto fire = new Fire(25, 9);
    auto badguy0 = new BadGuy(15, 4);
    auto badguy1 = new BadGuy(25, 5);

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

