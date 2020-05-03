#include "domain/bad_guy.cpp"
#include "domain/fire.cpp"
#include "domain/hero.cpp"
#include "domain/indian_team.cpp"
#include "domain/indian.cpp"
#include "domain/world.cpp"
#include "domain/warrior.cpp"
#include "app/terminal.cpp"

int main() {
    auto game = new Terminal(0);

    game->createWorld();

    game->draw();

    while(!game->world->isDestroyed()){
        game->input();
        game->world->nextIteration();
        game->draw();
    }

    return 0;
}
