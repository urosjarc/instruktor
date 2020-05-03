
#include "app/game.h"

void Game::saveWorld() {

}

void Game::createWorld(){

    //Branje iz datoteke...
    //Na podlagi datotek ustvari domenski prostor...

    /*
     * USTVARJANJE TESTNEGA DOMENSTEGA PROSTORA
     */
    auto hero = new Hero(20, 7);

    auto world = new World(hero, 1, 1, 1, 1, 40, 15, 2 * 60);

    auto fire = new Fire(25, 9);
    auto badguy0 = new BadGuy(15, 4);
    auto badguy1 = new BadGuy(25, 5);

    auto indianTeam0 = new IndianTeam(10, 10);
    auto indianTeam1 = new IndianTeam(5, 5);
    auto indianTeam2 = new IndianTeam(30, 30);

    world->badGuys.push_back(badguy0);
    world->badGuys.push_back(badguy1);

    world->indianTeams.push_back(indianTeam0);
    world->indianTeams.push_back(indianTeam1);
    world->indianTeams.push_back(indianTeam2);

    world->fires.push_back(fire);

    this->world = world;

    /**
     * ========================================
     */
}

void Game::draw() {

}

void Game::input() {

}
void Game::close() {

}

Game::Game(int level) {
    this->level = level;
}


