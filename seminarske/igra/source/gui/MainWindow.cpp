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

    //https://stackoverflow.com/questions/35400767/connecting-a-button-in-qt
    connect(ui.closePB, &QPushButton::clicked, this, &MainWindow::closeGame);
    connect(ui.newGamePB, &QPushButton::clicked, this, &MainWindow::newGame);
    connect(ui.loadPB, &QPushButton::clicked, this, &MainWindow::loadGame);

    window->loadScores();
    ui.scoreTE->clear();
    std::string line;
    for(auto s: window->scores){
        line.append(std::to_string(s->score));
        line.append("\t");
        line.append(s->name);
        line.append("\t");
        line.append(s->date);
        line.append("\n");
    }
    ui.scoreTE->setPlainText(QString::fromStdString(line));

    show();

}

void MainWindow::closeGame() {
    window->writeScores();
    window->saveWorld();
    window->close();
    QCoreApplication::processEvents();
}

void MainWindow::loadGame() {
    window->init();
    window->createWorld();
    window->world->hero->name = ui.uporabnikLE->text().toStdString();
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
    closeGame();
}

void MainWindow::newGame() {
    window->deleteSave();
    window->level = 1;
    loadGame();
}

