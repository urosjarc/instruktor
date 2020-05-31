
#include "app/events.h"
#include "app/game.h"

void Game::saveWorld() {
    
}

void Game::createWorld(){

    //Branje iz datoteke...
    //Na podlagi datotek ustvari domenski prostor...

    /*
     * USTVARJANJE TESTNEGA DOMENSTEGA PROSTORA
     */
    int height = 40 + 4 * level;
    int width = 15 + 4 * level;
    auto hero = new Hero(int (height / 2), int(width / 2));
    //World::World(Hero *hero, int fireIndex, int badGuysIndex, int indiansIndex, int waterIndex, int width, int height, int secondsToLive)
    auto world = new World(hero, level, level, level, level, height, width, level* 2 * 60); 

    for (int i = 0; i < pow(level, 2); i++) {
        auto badguy0 = new BadGuy(rand()%(world->width -0)+0 , rand()% world->height);
        world->badGuys.push_back(badguy0);
    }

    for (int i = 0; i < (level* 2); i++) {
        auto fire = new Fire(rand() % world->width , rand() % world->height);
        world->fires.push_back(fire);
    }
    for (int i = 0; i < (level+2); i++) {
    auto indianTeam0 = new IndianTeam(rand() % world->width, rand() % world->height);
    world->indianTeams.push_back(indianTeam0);
    }

    this->world = world;

    /**
     * ========================================
     */
}

void Game::draw() {

}

Event Game::input() {
    return Event::noInput;
}
void Game::close() {

}

Game::Game(int level) {
    this->level = level;
}


