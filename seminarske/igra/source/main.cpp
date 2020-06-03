#include "gui/MainWindow.h"

int main(int argc, char* argv[]) {
    /**
     * Qt5
     * https://doc.qt.io/qt-5/qtwidgets-mainwindows-application-example.html
     * youtube: c++ qt5
     * https://build-system.fman.io/qt-designer-download
     */
    QApplication app(argc, argv);
    auto* mainWindow = new MainWindow();
    int exit = QApplication::exec();
    return exit;
}

