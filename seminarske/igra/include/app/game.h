//
// Created by urosjarc on 3. 05. 20.
//

#ifndef IGRA_GAME_H
#define IGRA_GAME_H

#include "../../include/domain/world.h"
#include <fstream>

using namespace std;

class Game {
public:
   // fstream herosave();
    //fstream forest();
    //fstream badguys();
   // fstream goodguys();
    Game(int level=1);

    int level;
    World *world;

    virtual void saveWorld();
    virtual void draw();
    virtual Event input();
    virtual void close();
    virtual void createWorld();
};

#endif //IGRA_GAME_H
