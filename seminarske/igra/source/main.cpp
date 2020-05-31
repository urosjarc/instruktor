#include "gui/MainWindow.h"

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    auto* mainWindow = new MainWindow();
    int exit = QApplication::exec();
    return exit;
}

