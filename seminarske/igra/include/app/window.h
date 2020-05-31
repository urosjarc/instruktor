//
// Created by urosjarc on 3. 05. 20.
//

#ifndef IGRA_WINDOW_H
#define IGRA_WINDOW_H

#include "game.h"
#include <SDL2/SDL.h>

class Window: public Game {
public:
    Window(int level);

    SDL_Window* window;
    SDL_Renderer* renderer;

    int width = 600;
    int height = 400;

    void close() override ;
    void createWorld() override ;
    void draw() override ;
    Event input() override ;

};

#endif //IGRA_WINDOW_H
