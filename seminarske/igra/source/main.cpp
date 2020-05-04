#include <app/events.h>
#include "app/window.h"
#include "app/terminal.h"

int main() {
    auto game = new Window(0);

    game->createWorld();
    game->draw();

    Event input = Event::noInput;

    while(!game->world->isDestroyed() && input != Event::end){
        input = game->input();
        if(input == Event::input){
            game->world->nextIteration();
            game->draw();
        }
    }

    game->saveWorld();
    game->close();

    return 0;
}

