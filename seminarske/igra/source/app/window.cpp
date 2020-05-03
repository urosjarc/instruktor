
#include <cmath>
#include <iostream>
#include <SDL2/SDL.h>
#include <app/colours.h>
#include "app/window.h"
#include "app/simbols.h"

using namespace std;

void Window::close() {
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(this->window);
    SDL_Quit();
}

void Window::draw() {
    SDL_RenderClear( renderer );

    for (int y = 0; y < this->world->height; ++y) {
        for (int x = 0; x < this->world->width; ++x) {

            if (x == this->world->hero->x && y == this->world->hero->y) {
                SDL_Rect *r;
                r->w = (int) ((float) this->width) / this->world->width;
                r->h = (int) ((float) this->height) / this->world->height;
                r->x = (int) x*r->w;
                r->y = (int) y*r->h;
                SDL_SetRenderDrawColor( Window::renderer,hero[0], hero[1], hero[2], 255 );
                SDL_RenderFillRect( Window::renderer, r );
                continue;
            }

            /**
             * Draw badguys
             */
            bool isBadGuy = false;
            for (int i = 0; i < this->world->badGuys.size(); ++i) {
                if (x == this->world->badGuys[i]->x && y == this->world->badGuys[i]->y) {
                    isBadGuy = true;
                    break;
                }
            }
            if (isBadGuy) continue;

            /**
             * Draw indian teams & indians
             */
            bool isIndianTeam = false;
            for (int i = 0; i < this->world->indianTeams.size(); ++i) {
                if (x == this->world->indianTeams[i]->x && y == this->world->indianTeams[i]->y) {
                    isIndianTeam = true;
                    break;
                }

                for (int j = 0; j < this->world->indianTeams[i]->indians.size(); ++j) {
                    auto pIndian = this->world->indianTeams[i]->indians[j];
                    if (pIndian->x == x && pIndian->y == y) {
                        break;
                    }
                }
            }
            if (isIndianTeam) continue;

            /**
             * Draw fire
             */
            bool isFire = false;
            for (int i = 0; i < this->world->fires.size(); ++i) {
                float dx = this->world->fires[i]->x - x;
                float dy = this->world->fires[i]->y - y;
                float dist = pow(pow(dx, 2) + pow(dy, 2), 0.5); // (dx^2 + dy^2)^(1/2)

                if (dist < this->world->fires[i]->radius) {
                    isFire = true;
                    break;
                }
            }
            if (isFire) continue;

        }
    }

    SDL_RenderPresent(renderer);
    SDL_Delay(500);
}

void Window::input() {
    int dx, dy;

    cout << "Vnesi hero->dx: ";
    cin >> dx;

    cout << "Vnesi hero->dy: ";
    cin >> dy;

    this->world->hero->move(dx, dy);
}

void Window::createWorld() {
    Game::createWorld();
}

Window::Window(int level) : Game(level) {
    SDL_Init(SDL_INIT_VIDEO);
    window = SDL_CreateWindow( "The Game", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, SDL_WINDOW_SHOWN );
    renderer =  SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    SDL_SetRenderDrawColor( renderer, 0,0,0,0);
    SDL_SetRenderDrawColor(renderer, 100, 149, 237, 255);
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);
    SDL_Delay(5000);
}
