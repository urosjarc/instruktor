
#include <iostream>
#include <cmath>

#include "app/terminal.h"
#include "app/simbols.h"

using namespace std;

void Terminal::draw() {
    for (int y = 0; y < this->world->height; ++y) {
        for (int x = 0; x < this->world->width; ++x) {
            if (x == this->world->hero->x && y == this->world->hero->y) {
                cout << (char) hero;
                continue;
            }

            /**
             * Draw badguys
             */
            bool isBadGuy = false;
            for (int i = 0; i < this->world->badGuys.size(); ++i) {
                if (x == this->world->badGuys[i]->x && y == this->world->badGuys[i]->y) {
                    cout << (char) badGuy;
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
                    cout << (char) indianTeam;
                    isIndianTeam = true;
                    break;
                }

                for (int j = 0; j < this->world->indianTeams[i]->indians.size(); ++j) {
                    auto pIndian = this->world->indianTeams[i]->indians[j];
                    if(pIndian->x == x && pIndian->y == y) {
                        cout << (char) indian;
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
                    cout << (char) fire;
                    isFire = true;
                    break;
                }
            }
            if (isFire) continue;

            cout << (char) tree;
        }
        cout << endl;
    }
}

void Terminal::input() {
    int dx, dy;

    cout << "Vnesi hero->dx: ";
    cin >> dx;

    cout << "Vnesi hero->dy: ";
    cin >> dy;

    this->world->hero->move(dx, dy);
}

void Terminal::createWorld() {
    Game::createWorld();
}

void Terminal::close() {
    Game::createWorld();
}

Terminal::Terminal(int level) : Game(level) {
}

