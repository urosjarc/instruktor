#ifndef SPK_MAINWINDOW_H
#define SPK_MAINWINDOW_H

#include <QMainWindow>
#include <QApplication>
#include <QThread>
#include "app/window.h"
#include "gui/ui_MainWindow.h"
#include "gui/MainWindow.h"

class MainWindow: public QMainWindow {

public:
    Window* window;
    MainWindow(QWidget* parent = nullptr);
    void closeGame();
    void newGame();
    void loadGame();
private:
    Ui::MainWindow ui;
};

#endif //SPK_MAINWINDOW_H
