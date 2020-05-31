#include <QMenu>
#include <iostream>
#include <app/utils.h>
#include <ctime>
#include <cstdlib>
#include <app/events.h>
#include "app/window.h"
#include <QDebug>
#include <QPushButton>

#include "gui/MainWindow.h"
#include "gui/ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    ui.setupUi(this);

    srand(mix(clock(), time(NULL), NULL));

    connect(ui.closePB, &QPushButton::clicked, this, &MainWindow::close);
    connect(ui.newGamePB, &QPushButton::clicked, this, &MainWindow::newGame);
    connect(ui.loadPB, &QPushButton::clicked, this, &MainWindow::loadGame);
    connect(ui.replayPB, &QPushButton::clicked, this, &MainWindow::replay);
    show();

}

void MainWindow::close() {
    game->close();
    game->saveWorld();
}

void MainWindow::replay() {
    qDebug() << "replay";
}

void MainWindow::loadGame() {
    game = new Window(1);
    game->createWorld();
    game->draw();

    Event input = Event::noInput;

    while (!game->world->isDestroyed()) {
        QCoreApplication::processEvents();
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

    game->deleteSave();
    game->close();
}

void MainWindow::newGame() {
    game->deleteSave();
    loadGame();
}

