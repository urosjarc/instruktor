//
// Created by urosjarc on 3. 05. 20.
//

#ifndef IGRA_GAME_H
#define IGRA_GAME_H

#include "../domain/world.h"

class Game {
public:
    Game(int level) {
        this->level = level;
    }

    int level;
    World *world;

    void saveWorld();

    void draw();

    void input();

    void createWorld();
};

#endif //IGRA_GAME_H
