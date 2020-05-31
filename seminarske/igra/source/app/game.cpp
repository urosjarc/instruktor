
#include <iostream>
#include <cmath>
#include "app/events.h"
#include "app/game.h"

void Game::saveWorld() {
    ofstream f;
    ofstream f_indian;

    /**
     * LOAD info
     */
    f.open("info.txt");
    f << 1;
    f.close();

    /**
     * Save hero
     */
    f.open("hero.txt");
    f << (int) world->hero->isAlive
      << " " << world->hero->reputation
      << " " << world->hero->x
      << " " << world->hero->y
      << " " << (int) world->hero->invincible
      << " " << world->hero->invincibleRadius
      << " " << world->hero->killRadius;
    f.close();

    /**
     *
     */
    f.open("world.txt");
    f << world->fireIndex
      << " " << world->badGuysIndex
      << " " << world->indiansIndex
      << " " << world->waterIndex
      << " " << world->width
      << " " << world->height
      << " " << world->iterationsToLive
      << " " << world->iterationsRunning;
    f.close();

    /**
     * FIRE
     */
    f.open("fires.txt");
    f.close();
    f.open("fires.txt", ios::app);
    for (auto it: this->world->fires) {
        f << it->y << " "
          << it->x << " "
          << it->radius << " "
          << it->isAlive << "\n";
    }
    f.close();

    /**
     * TREES
     */
    f.open("trees.txt");
    f.close();
    f.open("trees.txt", ios::app);
    for (auto it: this->world->trees) {
        f << it->y << " "
          << it->x << " "
          << it->isAlive << "\n";
    }
    f.close();
    /**
     * BAD_GUY
     */
    f.open("bad_guys.txt");
    f.close();
    f.open("bad_guys.txt", ios::app);
    for (auto it: this->world->badGuys) {
        f << it->y << " "
          << it->x << " "
          << it->killRadius << " "
          << it->invincibleRadius << "\n";
    }
    f.close();

    /**
     * INDIANS & INDIAN TEAM
     */
    f.open("indianTeams.txt");
    f.close();
    f_indian.open("indian.txt");
    f_indian.close();

    f.open("indianTeams.txt", ios::app);

    int team = 0;
    for (auto it: this->world->indianTeams) {
        f << it->x << " "
          << it->y << "\n";

        f_indian.open("indian.txt", ios::app);
        for (auto indian: it->indians) {

            f_indian
                    << team << " "
                    << indian->x << " "
                    << indian->y << " "
                    << indian->seeingRadius << " "
                    << indian->invincibleRadius << " "
                    << indian->killRadius << " "
                    << (int) indian->invincible << " "
                    << indian->panicMode << "\n";
        }
        f_indian.close();
        team++;
    }
    f.close();
}

void Game::loadWorld() {
    ifstream f;

    /**
     * Save hero
     */
    int x;
    int y;
    int invincibleRadius;
    int isAlive;
    int reputation;
    int invincible;
    int killRadius;

    f.open("hero.txt");
    f >> isAlive >> reputation >> x >> y >> invincible >> invincibleRadius >> killRadius;

    auto hero = new Hero(x, y, invincibleRadius);
    hero->isAlive = (bool) isAlive;
    hero->reputation = reputation;
    hero->invincible = (bool) invincible;
    hero->killRadius = killRadius;
    f.close();

    /**
     * WORLD
     */
    int fireIndex;
    int badGuysIndex;
    int indiansIndex;
    int waterIndex;
    int width;
    int height;
    int iterationsToLive;
    int iterationsRunning;

    f.open("world.txt");
    f >> fireIndex >> badGuysIndex >> indiansIndex >> waterIndex >> width >> height >> iterationsToLive
      >> iterationsRunning;
    f.close();

    this->world = new World(hero, fireIndex, badGuysIndex, indiansIndex, waterIndex, width, height, iterationsToLive);
    this->world->iterationsRunning = iterationsRunning;


    /**
     * FIRES
     */
    f.open("fires.txt");
    float radius;
    while (f >> y >> x >> radius >> isAlive) {
        auto fire = new Fire(x, y);
        fire->isAlive = isAlive;
        fire->radius = radius;
        world->fires.push_back(fire);
    }
    f.close();

    /**
     * TREES
     */
    f.open("trees.txt");
    while (f >> y >> x >> isAlive) {
        auto tree = new Tree(x, y);
        tree->isAlive = isAlive;
        world->trees.push_back(tree);
    }
    f.close();

    /**
     * BAD_GUY
     */
    f.open("bad_guys.txt");
    while (f >> y >> x >> killRadius >> invincibleRadius) {
        auto badGuy = new BadGuy(x, y, invincibleRadius);
        badGuy->killRadius = killRadius;
        world->badGuys.push_back(badGuy);
    }
    f.close();

    /**
     * INDIAN TEAM
     */
    f.open("indianTeams.txt");
    while (f >> x >> y) {
        auto indianTeam = new IndianTeam(x, y);
        world->indianTeams.push_back(indianTeam);
    }
    f.close();

    /**
     * INDIANS
     */
    f.open("indians.txt");
    int team;
    int seeingRadius;
    int panicMode;
    while (f >> team >> x >> y >> seeingRadius >> invincibleRadius >> killRadius >> invincible >> panicMode) {
        auto indian= new Indian(x, y);
        indian->killRadius = killRadius;
        indian->invincible = invincible;
        indian->invincibleRadius = invincibleRadius;
        indian->panicMode = panicMode;
        indian->seeingRadius = seeingRadius;
        world->indianTeams[team]->indians.push_back(indian);
    }
    f.close();
}

void Game::createWorld() {

    ifstream f;

    /**
     * LOAD info
     */
    f.open("info.txt");
    int load;
    f >> load;
    f.close();

    std::cout << "Load world: " << load;

    if (load == 1) return Game::loadWorld();

    //Branje iz datoteke...
    //Na podlagi datotek ustvari domenski prostor...

    /*
     * USTVARJANJE TESTNEGA DOMENSTEGA PROSTORA
     */
    int height = 40 + 4 * level;
    int width = 15 + 4 * level;
    auto hero = new Hero(int(height / 2), int(width / 2));
    //World::World(Hero *hero, int fireIndex, int badGuysIndex, int indiansIndex, int waterIndex, int width, int height, int secondsToLive)
    auto world = new World(hero, level, level, level, level, height, width, level * 1000);

    for (int i = 0; i < pow(level, 2); i++) {
        auto badguy0 = new BadGuy(rand() % (world->width - 0) + 0, rand() % world->height);
        world->badGuys.push_back(badguy0);
    }

    for (int i = 0; i < (level * 2); i++) {
        auto fire = new Fire(rand() % world->width, rand() % world->height);
        world->fires.push_back(fire);
    }
    for (int i = 0; i < (level + 2); i++) {
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
void Game::deleteSave() {
    ofstream f;
    f.open("info.txt");
    f << 0;
    f.close();
}

Game::Game(int level) {
    this->level = level;
}


