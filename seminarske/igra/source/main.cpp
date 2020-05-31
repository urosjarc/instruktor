#include <app/utils.h>
#include <ctime>
#include <cstdlib>
//#include <SDL2/SDL.h>
#include <app/events.h>
//#include "app/window.h"
#include "app/terminal.h"

int main(int argc, char* argv[]) {
    srand(mix(clock(), time(NULL), NULL));
    auto game = new Terminal(1);

    game->createWorld();
    game->draw();

    Event input = Event::noInput;

    while(!game->world->isDestroyed() && input != Event::end){
        input = game->input();
        if(input == Event::input){
            game->world->nextIteration();
            if (game->world->checkForNextLevel()) {
                game->level++;
                game->createWorld();   
            }

            game->draw();
        }
    }

    game->saveWorld();
    game->close();

    return 0;
}

