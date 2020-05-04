//
// Created by urosjarc on 3. 05. 20.
//

#ifndef IGRA_TERMINAL_H
#define IGRA_TERMINAL_H

#include "game.h"

class Terminal: public Game {
public:
    Terminal(int level);
    void createWorld() override ;
    void draw() override ;
    void close() override ;
    Event input() override ;
};

#endif //IGRA_TERMINAL_H
