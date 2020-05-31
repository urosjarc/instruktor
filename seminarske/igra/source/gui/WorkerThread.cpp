//
// Created by urosjarc on 31. 05. 20.
//
#include <QThread>
#include <iostream>
#include <app/utils.h>
#include <ctime>
#include <cstdlib>
#include <app/events.h>
#include "app/window.h"
#include "gui/WorkerThread.h"

void WorkerThread::run() {
    QString result;
    srand(mix(clock(), time(NULL), NULL));
    auto game = new Window(1);

    game->createWorld();
    game->draw();

    Event input = Event::noInput;

    while (!game->world->isDestroyed() && input != Event::end) {
        input = game->input();
        if (input == Event::input) {
            game->world->nextIteration();
            if (game->world->checkForNextLevel()) {
                game->level++;
                game->deleteSave();
                game->createWorld();
            }

            game->draw();
        }
    }

    if (input == Event::end) game->saveWorld();
    else {
        game->deleteSave();
        game->close();
    }
}

