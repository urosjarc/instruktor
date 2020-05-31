#ifndef SPK_MAINWINDOW_H
#define SPK_MAINWINDOW_H

#include <QMainWindow>
#include <QApplication>
#include <QThread>
#include "app/game.h"
#include "gui/ui_MainWindow.h"
#include "gui/MainWindow.h"

class MainWindow: public QMainWindow {

public:
    Game* game;
    MainWindow(QWidget* parent = nullptr);
    void play();
    void replay();
    void close();
    void newGame();
    void loadGame();
private:
    Ui::MainWindow ui;
};

#endif //SPK_MAINWINDOW_H
