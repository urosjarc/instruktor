//
// Created by urosjarc on 3. 05. 20.
//

#ifndef IGRA_WINDOW_H
#define IGRA_WINDOW_H

#include <SDL2/SDL.h>
#include "domain/world.h"
#include "app/events.h"
#include "app/score.h"

class Window {
public:
    int level=1;
    World *world{};
    std::vector<Score*> scores;

    SDL_Window* window{};
    SDL_Renderer* renderer{};

    int width = 600;
    int height = 400;

    void init();
    void close();
    void createWorld();
    void draw();
    Event input();
    void replay();
    void deleteSave();
    void saveWorld();

    void loadWorld();

    void sortScores();
    void loadScores();
    void writeScores();
};

#endif //IGRA_WINDOW_H
