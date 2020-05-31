#include <app/utils.h>
#include <ctime>
#include <cstdlib>
#include <app/events.h>
#include "app/window.h"
#include "app/terminal.h"

int main(int argc, char* argv[]) {
    srand(mix(clock(), time(NULL), NULL));
    auto game = new Window(1);

    game->createWorld();
    game->draw();

    Event input = Event::noInput;

    while(!game->world->isDestroyed() && input != Event::end){
        input = game->input();
        if(input == Event::input){
            game->world->nextIteration();
            if (game->world->checkForNextLevel()) {
                game->level++;
                game->deleteSave();
                game->createWorld();   
            }

            game->draw();
        }
    }

    if(input==Event::end) game->saveWorld();
    else {
        game->deleteSave();
        game->close();
    }

    return 0;
}

