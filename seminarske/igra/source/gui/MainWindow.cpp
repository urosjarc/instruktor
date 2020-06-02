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

    window = new Window();

    srand(mix(clock(), time(NULL), NULL));

    connect(ui.closePB, &QPushButton::clicked, this, &MainWindow::closeGame);
    connect(ui.newGamePB, &QPushButton::clicked, this, &MainWindow::newGame);
    connect(ui.loadPB, &QPushButton::clicked, this, &MainWindow::loadGame);
    show();

}

void MainWindow::closeGame() {
    window->saveWorld();
    window->close();
    QCoreApplication::processEvents();
}

void MainWindow::loadGame() {
    window->init();
    window->createWorld();
    window->draw();

    Event input = Event::noInput;

    while (!window->world->isDestroyed()) {
        QCoreApplication::processEvents();
        input = window->input();
        if (input == Event::input) {
            window->world->nextIteration();
            if (window->world->checkForNextLevel()) {
                window->level++;
                window->deleteSave();
                window->replay();
                window->createWorld();
            }

            window->draw();
        }
    }

    window->deleteSave();
    window->close();
}

void MainWindow::newGame() {
    window->deleteSave();
    loadGame();
}

