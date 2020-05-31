#define SDL_MAIN_HANDLED
#include <cmath>
#include <iostream>
//#include <SDL2/SDL.h>
#include "../../include/app/colours.h"
#include "../../include/app/events.h"
#include "../../include/app/window.h"
#include "../../include/app/simbols.h"
/*
void Window::close() {
    SDL_DestroyRenderer(this->renderer);
    SDL_DestroyWindow(this->window);
    SDL_Quit();
}

void Window::draw() {

    SDL_SetRenderDrawColor( this->renderer, tree[0], tree[1], tree[2], 255);
    SDL_RenderClear( this->renderer );

    for (int y = 0; y < this->world->height; ++y) {
        for (int x = 0; x < this->world->width; ++x) {

            if (x == this->world->hero->x && y == this->world->hero->y) {
                SDL_Rect r = SDL_Rect();
                r.w = (int) ((float) this->width) / this->world->width;
                r.h = (int) ((float) this->height) / this->world->height;
                r.x = (int) x*r.w;
                r.y = (int) y*r.h;
                SDL_SetRenderDrawColor( this->renderer,hero[0], hero[1], hero[2], 255 );
                SDL_RenderFillRect( this->renderer, &r );
                continue;
            }

            bool isBadGuy = false;
            for (int i = 0; i < this->world->badGuys.size(); ++i) {
                if (x == this->world->badGuys[i]->x && y == this->world->badGuys[i]->y) {
                    SDL_Rect r = SDL_Rect();
                    r.w = (int) ((float) this->width) / this->world->width;
                    r.h = (int) ((float) this->height) / this->world->height;
                    r.x = (int) x*r.w;
                    r.y = (int) y*r.h;
                    SDL_SetRenderDrawColor( this->renderer,badGuy[0], badGuy[1], badGuy[2], 255 );
                    SDL_RenderFillRect( this->renderer, &r );
                    isBadGuy = true;
                    break;
                }
            }
            if (isBadGuy) continue;


            bool isIndianTeam = false;
            for (int i = 0; i < this->world->indianTeams.size(); ++i) {
                if (x == this->world->indianTeams[i]->x && y == this->world->indianTeams[i]->y) {
                    SDL_Rect r = SDL_Rect();
                    r.w = (int) ((float) this->width) / this->world->width;
                    r.h = (int) ((float) this->height) / this->world->height;
                    r.x = (int) x*r.w;
                    r.y = (int) y*r.h;
                    SDL_SetRenderDrawColor( this->renderer,indianTeam[0], indianTeam[1], indianTeam[2], 255 );
                    SDL_RenderFillRect( this->renderer, &r );
                    isIndianTeam = true;
                    break;
                }

                for (int j = 0; j < this->world->indianTeams[i]->indians.size(); ++j) {
                    auto pIndian = this->world->indianTeams[i]->indians[j];
                    if (pIndian->x == x && pIndian->y == y) {
                        SDL_Rect r = SDL_Rect();
                        r.w = (int) ((float) this->width) / this->world->width;
                        r.h = (int) ((float) this->height) / this->world->height;
                        r.x = (int) x*r.w;
                        r.y = (int) y*r.h;
                        SDL_SetRenderDrawColor( this->renderer,indian[0], indian[1], indian[2], 255 );
                        SDL_RenderFillRect( this->renderer, &r );
                        break;
                    }
                }
            }
            if (isIndianTeam) continue;


            bool isFire = false;
            for (int i = 0; i < this->world->fires.size(); ++i) {
                float dx = this->world->fires[i]->x - x;
                float dy = this->world->fires[i]->y - y;
                float dist = pow(pow(dx, 2) + pow(dy, 2), 0.5); // (dx^2 + dy^2)^(1/2)

                if (dist < this->world->fires[i]->radius) {
                    SDL_Rect r = SDL_Rect();
                    r.w = (int) ((float) this->width) / this->world->width;
                    r.h = (int) ((float) this->height) / this->world->height;
                    r.x = (int) x*r.w;
                    r.y = (int) y*r.h;
                    SDL_SetRenderDrawColor( this->renderer,fire[0], fire[1], fire[2], 255 );
                    SDL_RenderFillRect( this->renderer, &r );
                    isFire = true;
                    break;
                }
            }
            if (isFire) continue;

        }
    }

    SDL_RenderPresent(this->renderer);
}

Event Window::input() {

    SDL_Event event = SDL_Event();
    while( SDL_PollEvent( &event ) ){
        switch( event.type ){
            // Look for a keypress 
            case SDL_KEYDOWN:
                // Check the SDLKey values and move change the coords 
                switch( event.key.keysym.sym ){
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
                    case SDLK_END:
                        return Event::end;
                    default:
                        return Event::noInput;
                }
        }
    }

    return Event::noInput;
}

void Window::createWorld() {
    Game::createWorld();
}

Window::Window(int level) : Game(level) {
    SDL_Init(SDL_INIT_VIDEO);
    this->window = SDL_CreateWindow( "The Game", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, SDL_WINDOW_SHOWN );
    this->renderer =  SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
}
*/