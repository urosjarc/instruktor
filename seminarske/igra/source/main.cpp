#include <iostream>
#include "app/window.h"
#include "app/terminal.h"

using namespace std;

int main() {
    auto game = new Window(0);


    game->createWorld();
    game->draw();

    while(!game->world->isDestroyed()){
        game->input();
        game->world->nextIteration();
        game->draw();
    }

    game->saveWorld();
    game->close();


    return 0;
}
