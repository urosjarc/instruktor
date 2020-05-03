//
// Created by urosjarc on 3. 05. 20.
//

#ifndef IGRA_TERMINAL_H
#define IGRA_TERMINAL_H

#include "game.h"

class Terminal: Game {
public:
    Terminal(int level) : Game(level) {
        this->createWorld();
    }
    void createWorld();
    void draw();
    void input();
};

#endif //IGRA_TERMINAL_H
