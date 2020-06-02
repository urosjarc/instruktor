#include <cmath>
#include <SDL2/SDL.h>
#include <iostream>
#include <algorithm>
#include <QtCore/qlogging.h>
#include "app/colours.h"
#include "app/events.h"
#include "app/window.h"

void Window::close() {
    SDL_DestroyRenderer(this->renderer);
    SDL_DestroyWindow(this->window);
    SDL_Quit();
}

void Window::init() {
    SDL_Init(SDL_INIT_VIDEO);
    this->window = SDL_CreateWindow("The Game", 0, 0, width, height,
                                    SDL_WINDOW_SHOWN);
    this->renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
}

void Window::replay() {
    auto score = new Score( world->hero->name,world->hero->reputation);
    scores.push_back(score);
    sortScores();
    for (auto p: this->world->hero->history) {
        SDL_SetRenderDrawColor(this->renderer, tree[0], tree[1], tree[2], 255);
        SDL_RenderClear(this->renderer);

        for (int y = 0; y < this->world->height; ++y) {
            for (int x = 0; x < this->world->width; ++x) {

                if (x == p->x && y == p->y) {
                    SDL_Rect r = SDL_Rect();
                    r.w = (int) ((float) this->width) / this->world->width;
                    r.h = (int) ((float) this->height) / this->world->height;
                    r.x = (int) x * r.w;
                    r.y = (int) y * r.h;
                    SDL_SetRenderDrawColor(this->renderer, hero[0], hero[1], hero[2], 255);
                    SDL_RenderFillRect(this->renderer, &r);
                    continue;
                }

            }
        }

        SDL_RenderPresent(this->renderer);
        SDL_Delay(100);
    }
}

void Window::saveWorld() {
    std::ofstream f;
    std::ofstream f_indian;

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
      << " " << world->hero->name
      << " " << world->hero->killRadius;
    f.close();

    f.open("replay.txt");
    f.close();
    f.open("replay.txt", std::ios::app);
    for (auto it: this->world->hero->history) {
        f << it->y << " "
          << it->x << "\n";
    }
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
    f.open("fires.txt", std::ios::app);
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
    f.open("trees.txt", std::ios::app);
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
    f.open("bad_guys.txt", std::ios::app);
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

    f.open("indianTeams.txt", std::ios::app);

    int team = 0;
    for (auto it: this->world->indianTeams) {
        f << it->x << " "
          << it->y << "\n";

        f_indian.open("indian.txt", std::ios::app);
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

void Window::loadWorld() {
    std::ifstream f;

    /**
     * Save hero
     */
    int x;
    int y;
    int invincibleRadius;
    char name[10];
    int isAlive;
    int reputation;
    int invincible;
    int killRadius;

    f.open("hero.txt");
    f >> isAlive >> reputation >> x >> y >> invincible >> invincibleRadius >> name >> killRadius;

    auto hero = new Hero(x, y, invincibleRadius);
    hero->isAlive = (bool) isAlive;
    hero->reputation = reputation;
    hero->invincible = (bool) invincible;
    hero->killRadius = killRadius;
    hero->name = name;
    f.close();

    /**
     * REPLAY
     */

    f.open("replay.txt");
    while(f >> y >> x) {
        auto p = new Point(x, y);
        hero->history.push_back(p);
    }
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
        auto indian = new Indian(x, y);
        indian->killRadius = killRadius;
        indian->invincible = invincible;
        indian->invincibleRadius = invincibleRadius;
        indian->panicMode = panicMode;
        indian->seeingRadius = seeingRadius;
        world->indianTeams[team]->indians.push_back(indian);
    }
    f.close();
}

void Window::createWorld() {
    std::ifstream f;

    /**
     * LOAD info
     */
    f.open("info.txt");
    int load;
    f >> load;
    f.close();

    std::cout << "Load world: " << load;

    if (load == 1) return loadWorld();

    //Branje iz datoteke...
    //Na podlagi datotek ustvari domenski prostor...

    /*
     * USTVARJANJE TESTNEGA DOMENSTEGA PROSTORA
     */
    int height = 40 + 4 * level;
    int width = 15 + 4 * level;
    auto hero = new Hero(int(height / 2), int(width / 2));
    auto world = new World(hero, level, level, level, level, width, height, level * 1000);

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

void Window::deleteSave() {
    std::ofstream f;
    f.open("info.txt");
    f << 0;
    f.close();
}

void Window::draw() {

    SDL_SetRenderDrawColor(this->renderer, tree[0], tree[1], tree[2], 255);
    SDL_RenderClear(this->renderer);

    for (int y = 0; y < this->world->height; ++y) {
        for (int x = 0; x < this->world->width; ++x) {

            if (x == this->world->hero->x && y == this->world->hero->y) {
                SDL_Rect r = SDL_Rect();
                r.w = (int) ((float) this->width) / this->world->width;
                r.h = (int) ((float) this->height) / this->world->height;
                r.x = (int) x * r.w;
                r.y = (int) y * r.h;
                SDL_SetRenderDrawColor(this->renderer, hero[0], hero[1], hero[2], 255);
                SDL_RenderFillRect(this->renderer, &r);
                continue;
            }

            bool isBadGuy = false;
            for (auto &i : this->world->badGuys) {
                if (x == i->x && y == i->y) {
                    SDL_Rect r = SDL_Rect();
                    r.w = (int) ((float) this->width) / this->world->width;
                    r.h = (int) ((float) this->height) / this->world->height;
                    r.x = (int) x * r.w;
                    r.y = (int) y * r.h;
                    SDL_SetRenderDrawColor(this->renderer, badGuy[0], badGuy[1], badGuy[2], 255);
                    SDL_RenderFillRect(this->renderer, &r);
                    isBadGuy = true;
                    break;
                }
            }
            if (isBadGuy) continue;


            bool isIndianTeam = false;
            bool isIndian = false;
            for (auto &i : this->world->indianTeams) {
                if (x == i->x && y == i->y) {
                    SDL_Rect r = SDL_Rect();
                    r.w = (int) ((float) this->width) / this->world->width;
                    r.h = (int) ((float) this->height) / this->world->height;
                    r.x = (int) x * r.w;
                    r.y = (int) y * r.h;
                    SDL_SetRenderDrawColor(this->renderer, indianTeam[0], indianTeam[1], indianTeam[2], 255);
                    SDL_RenderFillRect(this->renderer, &r);
                    isIndianTeam = true;
                    break;
                }

                for (auto pIndian : i->indians) {
                    if (pIndian->x == x && pIndian->y == y) {
                        SDL_Rect r = SDL_Rect();
                        r.w = (int) ((float) this->width) / this->world->width;
                        r.h = (int) ((float) this->height) / this->world->height;
                        r.x = (int) x * r.w;
                        r.y = (int) y * r.h;
                        SDL_SetRenderDrawColor(this->renderer, indian[0], indian[1], indian[2], 255);
                        SDL_RenderFillRect(this->renderer, &r);
                        isIndian = true;
                        break;
                    }
                }
            }
            if (isIndianTeam || isIndian) continue;


            bool isFire = false;
            for (auto &i : this->world->fires) {
                int dx = i->x - x;
                int dy = i->y - y;
                auto dist = (float) pow(pow(dx, 2) + pow(dy, 2), 0.5); // (dx^2 + dy^2)^(1/2)

                if (dist < i->radius) {
                    SDL_Rect r = SDL_Rect();
                    r.w = (int) ((float) this->width) / this->world->width;
                    r.h = (int) ((float) this->height) / this->world->height;
                    r.x = (int) x * r.w;
                    r.y = (int) y * r.h;
                    SDL_SetRenderDrawColor(this->renderer, fire[0], fire[1], fire[2], 255);
                    SDL_RenderFillRect(this->renderer, &r);
                    isFire = true;
                    break;
                }
            }
            if (isFire) continue;

            for (Tree *it : this->world->trees) {
                if (it->x == x && it->y == y) {
                    if (!it->isAlive) {
                        SDL_Rect r = SDL_Rect();
                        r.w = (int) ((float) this->width) / this->world->width;
                        r.h = (int) ((float) this->height) / this->world->height;
                        r.x = (int) x * r.w;
                        r.y = (int) y * r.h;
                        SDL_SetRenderDrawColor(this->renderer, deadTree[0], deadTree[1], deadTree[2], 255);
                        SDL_RenderFillRect(this->renderer, &r);
                    }
                }

            }

        }
    }

    SDL_RenderPresent(this->renderer);
}

Event Window::input() {

    SDL_Event event = SDL_Event();
    while (SDL_PollEvent(&event)) {
        switch (event.type) {
            // Look for a keypress 
            case SDL_KEYDOWN:
                // Check the SDLKey values and move change the coords 
                switch (event.key.keysym.sym) {
                    case SDLK_LEFT:
                        this->world->hero->move(-1, 0);
                        return Event::input;
                    case SDLK_RIGHT:
                        this->world->hero->move(1, 0);
                        return Event::input;
                    case SDLK_UP:
                        this->world->hero->move(0, -1);
                        return Event::input;
                    case SDLK_DOWN:
                        this->world->hero->move(0, 1);
                        return Event::input;
                    case SDLK_ESCAPE:
                        return Event::end;
                    default:
                        return Event::noInput;
                }
        }
    }

    return Event::noInput;
}

void Window::sortScores() {
    std::sort(scores.begin(), scores.end(), [](Score* lhs, Score* rhs) {
        return lhs->score > rhs->score;
    });
}
void Window::writeScores(){
    std::ofstream f;
    f.open("scores.txt");
    for (auto it: scores) {
        f << it->score << " "
          << it->name << " "
          << it->date << "\n";
    }
    f.close();

}
void Window::loadScores() {
    std::ifstream f;
    int score;
    std::string name;
    std::string date;
    f.open("scores.txt");
    while(f >> score >> name >> date) {
        auto s = new Score(name, score, date);
        scores.push_back(s);
    }
    sortScores();
    f.close();
}

